from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import yaml
import re
import mysql.connector
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

from actions.api.endpoints import ENDPOINTS
from actions.api.text_responses import CLAIM_TEXT_RESPONSES

"""
1. Makes an API Call by passing
   Parameters:
   1. Claim ID
   2. Provider First Name
   3. Provider Last Name
   4. Provider NPI
   5. 0 - To get details from Local DB
      1 - To get details from Payer System(EDI Transaction)
2. Gets Claim Details from Local DB/Payer System
3. Returns "rsc", "csi_category_code" (Inquiry Category Code) and a text response from "CLAIM_TEXT_RESPONSES" dictionary corresponding to claim status
"""
class ClaimStatusInquiryAPI:

    def __init__(self):
        self.name = "hc_csi_api"
    
    def create_path(self, base, query, user_values):

        return (base+query).format(user_values["provider_first_name"], user_values["provider_last_name"], user_values["claim_id"], user_values["provider_npi"], user_values["fresh_request"])

    def get_category_code(self, rcc, rsc):
        
        print("Getting category code using RCC & RSC...")
        
        CATEGORY_CODES = {
            "A1": {
                "19": "1" # 123X456Y789Z0
            },
            "A2": {
                "3": "1",  # JDO9863741GHY
                "20":"1"}, # 123BH563GYU1
             "A4": {
                "33": "5", # BGEUDDTW8
                "35": "5"  # NHU12378D2
            },
            "A7": {
                "0": "5",    # R678DN3
                "29": "5",   # GFTYJWKDHH989
                "116": "5",  # BGD53737464
                "475": "2",  # 87767HSFG
                "454": "2"}, # HSJH7638
            "E1": {
                "484": "1"}, # XY1234567897Z
            "F1": {
                "65": "1",  # A1234567894
                "521": "8", # ABC876487564
                "47": "7"}, # SGF876678            
            "F2": {
                "81": "4",   # HBBH827659
                "84": "3",  # 63GDHSCN82
                "88": "4",  # GSFRW83635363
                "91": "3",  # HYE628274HD
                "780": "4", # 
                "585": "2", # AB1234567895C
                "674": "3"}, # 73638NDGSF83
            "F3": {
                "101": "6"}, # A1234567896BCD            
            "P0": {
                "38": "1",  # BFGFY6272837FD
                "44": "1",  # ADGYFT654J
                "685": "1", # NJUGFR583N
                "686": "1"},# NCHGSTDJ2936
            "P1": {
                "20": "1"} # ABCXYZ1234567899
        }
        
        category_code = CATEGORY_CODES[rcc][rsc]
        print(f"category_code: {category_code}")
        return category_code
            
    def get_text_response(self, api_values, user_values):

        print("getting corresponding text response")
        print(f"api_values:{api_values}")
        print(f"user_values:{user_values}")

        print(f'errorCode:{api_values["errorCode"]}')
        if api_values["errorCode"] == 1:
            return api_values["errorMessage"]
        else:
            RCC = api_values["responseCategoryCode"]
            RSC = api_values["responseStatusCode"]
            print(f"RCC:{RCC} RSC:{RSC}")
            exec(CLAIM_TEXT_RESPONSES[RCC][RSC], locals(), globals())

            # reject_reason = api_values["category"]
            # reject_reason = 1 [renamed to below]
            csi_category_code = "1"        
            # csi_category_code = self.get_category_code(RCC, RSC)

            return RSC, csi_category_code, text    

    def get_claim_status(self, claim_id, provider_first_name, provider_last_name, provider_npi, fresh_request):

        user_values = {'claim_id': claim_id, 'provider_first_name': provider_first_name, 'provider_last_name': provider_last_name, 'provider_npi': provider_npi, 'fresh_request': fresh_request}
        full_path = self.create_path(ENDPOINTS["base"], ENDPOINTS["claim_status_query"], user_values)
        try:
            print("making API Call")
            json_obj = requests.get(full_path).json()
            print(json_obj)
            data = json.dumps(json_obj)
            api_values = json.loads(data)
            rsc, csi_category_code, text_response = self.get_text_response(api_values, user_values)
            print("got text response in get_claim_status function")
            print(f"rsc:{rsc}")
            print(f"text response:{text_response}")
            print(f"csi_category_code:{csi_category_code}")
            return rsc, csi_category_code, text_response
        except:
            print("failed api call")
            print("empty list")
            return 0, 0, 0
    
    def get_db_check_type(self, code):

        """
        Set "db_check_type" based on slot - "sub_category_code" [CSI More Details Route-2]
        1: Only CSI [Claim Status: In Progress] 
        2: Payment [Claim Status: Rejected]
        3: Preauthorization [Claim Status: Rejected]
        4: Patient Benefits [Claim Status: Rejected]
        5: Administrative [Claim Status: Rejected]
        6: Over Paid [Claim Status: Approved]
        7: Partially Paid [Claim Status: Approved]
        8: Adjustment [Claim Status: Approved]        
        """
        # rri_codes_payment = ["585", "454", "12"]
        # rri_codes_payment=["103", "475", "488", "86", "454","596", "474", "585", "764"] # csi rejected claim - payment related codes
        rri_codes_payment=["475", "454", "585",] # csi rejected claim - payment related codes
        rri_codes_preauthorization = ["84", "91", "674"] # csi rejected claim - preauthorization related codes
        rri_codes_pbi = ["81", "88"] # csi rejected claim - patient benefits related codes
        rri_codes_admin = ["29", "33", "116"]
        aci_codes_over_paid = ["101"] # csi approved claim - over paid codes
        aci_codes_partially_paid = ["47"] # csi approved claim - partially paid codes
        aci_codes_adjustment = ["521"] # csi approved claim - adjustment codes

        CSI_SUB_CATEGORY_CODES ={ "2": rri_codes_payment,
                                  "3": rri_codes_preauthorization,
                                  "4": rri_codes_pbi,
                                  "5": rri_codes_admin,
                                  "6": aci_codes_over_paid,
                                  "7": aci_codes_partially_paid, 
                                  "8": aci_codes_adjustment
                                }  
        
        for key, value in CSI_SUB_CATEGORY_CODES.items():
            if code in value:
                print(key)
 
        return key