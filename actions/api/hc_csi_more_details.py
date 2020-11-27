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

"""
1. Makes an API Call to get more details of an approved/rejected claim by passing
   Parameters:
        1. Claim ID
        2. Provider First Name
        3. Provider Last Name
        4. Provider NPI
        5. CSI Category Code
        6. "0" - To get details from Local DB
           "1" - To get details from Payer System(EDI Transaction)
2. Gets More Details(Text Response) from Local DB/Payer System
3. Returns the text response
"""
class CSIMoreDetailsAPI:

    def __init__(self):
        self.name = "hc_csi_more_details_api"
    
    # Update this after API is ready to match the API params and user_values 
    def create_path(self, base, query, user_values):

        return (base+query).format(user_values["provider_first_name"], user_values["provider_last_name"], user_values["claim_id"],
                                   user_values["provider_npi"], user_values["fresh_request", user_values["csi_category_code"]])
    
    def get_more_details(self, claim_id, provider_first_name, provider_last_name, provider_npi, fresh_request, csi_category_code):

        user_values = {'claim_id': claim_id, 'provider_first_name': provider_first_name, 'provider_last_name': provider_last_name,
                        'provider_npi': provider_npi, 'fresh_request': fresh_request, 'csi_category_code': csi_category_code}
        full_path = self.create_path(ENDPOINTS["base"], ENDPOINTS["csi_more_details"], user_values)
        try:
            print("making API Call [CSI More Details]")
            json_obj = requests.get(full_path).json()
            print(json_obj)
            data = json.dumps(json_obj)
            api_values = json.loads(data)
            # text_response = api_values['text_response']
            text_response = "More Details from API"
            print("got text response in get_more_details function")
            print(f"text response:{text_response}")
            return text_response
        except:
            print("failed api call")
            print("empty list")
            return 0