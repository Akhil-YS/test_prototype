from .api.dbConn import check_local_db, store_user_details
# from .api.hc_pbi import PatientBenefitInquiryAPI [Not using for Prototype]    ]
from .api.hc_csi import ClaimStatusInquiryAPI
from .api.hc_csi_more_details import CSIMoreDetailsAPI
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import yaml
import re
# email libraries
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from email.message import EmailMessage
# from time import sleep
# mysql db libraries
import mysql.connector
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

# importing api file
# from .apiCSI import *
# from .dbConn import *


with open('actions/appConfig.yml') as test:
    val = yaml.safe_load(test)

# -------------------------Form Action - CSI Form-1 starts here-----------------------------------


class CSIDBCheckForm(FormAction):
    def name(self) -> Text:
        return 'csi_db_check_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['claim_id', 'provider_npi']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "claim_id": [
                self.from_entity(entity="claim_id"),
                self.from_text(intent="inform"),
            ],
            "provider_npi": [
                self.from_entity(entity="npi"),
                self.from_text(intent="inform"),
            ],
        }

    async def validate(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        slot_values = {}
        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(
                dispatcher, tracker, domain))

            if not slot_values:
                # reject to execute the form action
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(
                    self.name(),
                    f"Failed to extract slot {slot_to_fill} with action {self.name()}",
                )
        logger.debug(f"Validating extracted slots: {slot_values}")
        return await self.validate_slots(slot_values, dispatcher, tracker, domain)

    def validate_claim_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        regex = '^[a-zA-Z0-9]{1,50}$'
        check = bool(re.match(regex, value))
        print(f"Claim Validation Check:{check}")
        if(check):
            print("Claim ID check: Passed -> inside if")
            return {"claim_id": value}
        else:
            print("Claim ID check: Failed -> inside else")
            dispatcher.utter_message(text="The Claim ID entered is invalid,\
                claim ID is an Alphanum Identifier issued while the claim was submitted.")
            dispatcher.utter_message(text="Let's try again")
            return {"claim_id": None}

    def validate_provider_npi(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        regex = '^[0-9]{10}$'
        check = bool(re.match(regex, value))
        print(f"NPI Validation Check:{check}")
        if(check):
            print("NPI check: Passed -> inside if")
            return {"provider_npi": value}
        else:
            print("NPI check: Failed -> inside else")
            dispatcher.utter_message(text="Invalid NPI. NPI is a 10-digit number,\
                you may contact the facility administration team to know your NPI.")
            dispatcher.utter_message(text="Let's try again")
            return {"provider_npi": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        print(f"CSI DB Check form Memory:")
        print(f"Claim ID:{tracker.get_slot('claim_id')}")
        print(f"First Name:{tracker.get_slot('provider_first_name')}")
        print(f"Last Name:{tracker.get_slot('provider_last_name')}")
        print(f"NPI:{tracker.get_slot('provider_npi')}")
        print(f"Fresh Request:{tracker.get_slot('fresh_request')}")
        # dispatcher.utter_message(text="checking local DB...(in form 1)")
        return [FollowupAction('action_db_check')]

# --------------------------Form Action - CSI Form-1 ends here----------------------------------------------------------------

# --------------------------Form Action - CSI Form-2 starts here-------------------------------------------------------------


class CSIProviderNamesForm(FormAction):
    def name(self) -> Text:
        return 'csi_provider_names_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['provider_first_name', 'provider_last_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "provider_first_name": [
                self.from_entity(entity="name"),
                self.from_text(intent="inform"),
            ],
            "provider_last_name": [
                self.from_entity(entity="name"),
                self.from_text(intent="inform"),
            ],
        }

    async def validate(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        slot_values = {}
        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(
                dispatcher, tracker, domain))

            if not slot_values:
                # reject to execute the form action
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(
                    self.name(),
                    f"Failed to extract slot {slot_to_fill} with action {self.name()}",
                )
        logger.debug(f"Validating extracted slots: {slot_values}")
        return await self.validate_slots(slot_values, dispatcher, tracker, domain)

    def validate_provider_first_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        regex = '^[A-Za-z]{2,50}$'
        check = bool(re.match(regex, value))
        print(f"First Name Validation Check:{check}")
        if(check):
            print("First Name: Passed -> inside if")
            return {"provider_first_name": value}
        else:
            print("First Name: Failed -> inside else")
            dispatcher.utter_message(
                text="This looks like an invalid First Name.")
            dispatcher.utter_message(text="Let's try again")
            return {"provider_first_name": None}

    def validate_provider_last_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        regex = '^[A-Za-z]{2,50}$'
        check = bool(re.match(regex, value))
        print(f"Last Name Validation Check:{check}")
        if(check):
            print("Last Name: Passed -> inside if")
            return {"provider_last_name": value}
        else:
            print("Last Name: Failed -> inside else")
            dispatcher.utter_message(
                text="This looks like an invalid Last Name.")
            dispatcher.utter_message(text="Let's try again")
            return {"provider_last_name": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        print(f"Memory:")
        print(f"Claim ID:{tracker.get_slot('claim_id')}")
        print(f"First Name:{tracker.get_slot('provider_first_name')}")
        print(f"Last Name:{tracker.get_slot('provider_last_name')}")
        print(f"NPI:{tracker.get_slot('provider_npi')}")
        print(f"Fresh Request:{tracker.get_slot('fresh_request')}")
        print("CSI API form filled")
        # dispatcher.utter_message(text="checking local DB...(in form 2)")
        return []
# --------------------------Form Action - CSI API Form ends here-------------------------------------------


# Custom Action - DB Check.
class ActionDBCheck(Action):
    def name(self) -> Text:
        return "action_db_check"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("In action_db_check")

        claim_id = tracker.get_slot('claim_id')
        provider_npi = tracker.get_slot('provider_npi')

        db_check_type = 1  # 1: Claim Status Inquiry
        result, existing_details = check_local_db(claim_id, provider_npi, db_check_type)

        print(f"CSI local DB Check result:{result}")
        print(f"CSI existing details:{existing_details}")
        if result == 0:   # Claim ID does not exist in local DB
            print("Claim ID does not exist in local DB")
            exist_in_DB = "no"
            fresh_request = 1  # sending "1" to API
            return [SlotSet("exist_in_DB", exist_in_DB),
                    SlotSet("fresh_request", fresh_request)]
        else:   # Claim ID exists in local DB
            print("Claim ID exists in local DB")
            exist_in_DB = "yes"
            fresh_request = 0  # sending "0" to API
            print("CSI DB Check form filled")

            return [SlotSet("exist_in_DB", exist_in_DB),
                    SlotSet("fresh_request", fresh_request),
                    SlotSet("provider_first_name", existing_details[0]),
                    SlotSet("provider_last_name", existing_details[1]),
                    SlotSet("request_recency", existing_details[-1])]

# Custom Action - Fetch.
# Gets fresh claim status(details) with a fresh request to the Payer System.
class ActionCSIFetch(Action):
    def name(self) -> Text:
        return "action_csi_fetch"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("In action_csi_fetch")
        claim_id = tracker.get_slot('claim_id')
        provider_first_name = tracker.get_slot('provider_first_name')
        provider_last_name = tracker.get_slot('provider_last_name')
        provider_npi = tracker.get_slot('provider_npi')
        fresh_request = 0  # API Call to Local DB. [Ideally, update slot also?]
        api = ClaimStatusInquiryAPI()
        rsc, csi_category_code, result = api.get_claim_status(claim_id, provider_first_name, provider_last_name, provider_npi, fresh_request)
        print(f"rsc:{rsc}, csi_category_code:{csi_category_code}, result:{result}")
        if result == 0:
            dispatcher.utter_message(text="Error in API Call")
            return[]
        else:
            dispatcher.utter_message(result)

            # if reject_reason["type"] > 0:[Updated to below]
            print(f"int(csi_category_code): {int(csi_category_code)}, type(csi_category_code):{type(csi_category_code)}")
          
            if int(csi_category_code) > 1:
                csi_more_details = "yes"
            elif int(csi_category_code) == 1:
                csi_more_details = "no"

            return [SlotSet("csi_category_code", csi_category_code), SlotSet("csi_more_details", csi_more_details)]

# Custom Action - Refetch.
# Gets fresh claim status(details) with a fresh request to the Payer System.
class ActionCSIRefetch(Action):
    def name(self) -> Text:
        return "action_csi_refetch"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        claim_id = tracker.get_slot('claim_id')
        provider_first_name = tracker.get_slot('provider_first_name')
        provider_last_name = tracker.get_slot('provider_last_name')
        provider_npi = tracker.get_slot('provider_npi')
        # API Call to Payer System. [Ideally, update slot also?]
        fresh_request = 1
        api = ClaimStatusInquiryAPI()
        rsc, csi_category_code, result = api.get_claim_status(claim_id, provider_first_name, provider_last_name,
                                                           provider_npi, fresh_request)
        if result == 0:
            dispatcher.utter_message(text="Error in API Call")
            return[]
        else:
            dispatcher.utter_message(result)

            # if reject_reason["type"] > 0:[Updated to below]
            print(f"int(csi_category_code): {int(csi_category_code)}, type(csi_category_code):{type(csi_category_code)}")
          
            if int(csi_category_code) > 1:
                csi_more_details = "yes"
            elif int(csi_category_code) == 1:
                csi_more_details = "no"

            return [SlotSet("csi_category_code", csi_category_code), SlotSet("csi_more_details", csi_more_details)]

# Custom Action - More Details Buttons
# Displays buttons as per the claim status type in the UI.
class ActionCSIMoreDetailsButtons(Action):
    def name(self) -> Text:
        return "action_csi_more_details_buttons"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        csi_category_code = tracker.get_slot('csi_category_code')

        if csi_category_code == "1":
            dispatcher.utter_message( text="Error in CSI Story. This Claim ID shouldn't have more details [In Progress Category].")
        elif csi_category_code == "2":
            text_1 = "Hey, looks like the claim has been rejected at the payments house.\
                      Would you like to fetch more information on this rejection."
            button_resp_1 = [
                {
                    "title": "Fetch more payment details",
                    "payload": "/rri_payment"
                }
            ]
            text_2 = "Alternatively, would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Preauthorization",
                    "payload": "/rri_preauthorization"
                },
                {
                    "title": "Patient Benefit Info",
                    "payload": "/rri_pbi"
                }                
            ]
        elif csi_category_code == "3":
            text_1 = "Hey, looks like the claim has been rejected at the authorization house.\
                      Would you like to fetch more information on this rejection."
            button_resp_1 = [
                {
                    "title": "More Preauthorization details",
                    "payload": "/rri_preauthorization"
                }
            ]
            text_2 = "Alternatively,  would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Payment Info",
                    "payload": "/rri_payment"
                },
                {
                    "title": "Patient Benefit Info",
                    "payload": "/rri_pbi"
                }                   
            ]
        elif csi_category_code == "4":
            text_1 = "Hey, looks like the claim has been rejected for benefit coverage.\
                      Would you like to fetch more information on this rejection."
            button_resp_1 = [
                {
                    "title": "Fetch benefit coverage summary",
                    "payload": "/rri_pbi"
                }
            ]
            text_2 = "Alternatively,  would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Payment Info",
                    "payload": "/rri_payment"
                },
                {
                    "title": "Preauthorization",
                    "payload": "/rri_preauthorization"
                }              
            ]
        elif csi_category_code == "5":
            dispatcher.utter_message( text="Error in CSI Story. This Claim ID shouldn't have more details [In Progress Category].")       
        elif csi_category_code == "6":
            text_1 = "6. Statement for Over Paid"
            button_resp_1 = [
                {
                    "title": "Over Paid",
                    "payload": "/aci_over_paid"
                }
            ]
            text_2 = "Alternatively,  would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Partially Paid",
                    "payload": "/aci_partially_paid"
                },
                {
                    "title": "Adjustment",
                    "payload": "/aci_adjustment"
                }
            ]
        elif csi_category_code == "7":
            text_1 = "7. Statement for Partially Paid"
            button_resp_1 = [
                {
                    "title": "Partially Paid",
                    "payload": "/aci_partially_paid"
                }
            ]
            text_2 = "Alternatively,  would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Over Paid",
                    "payload": "/aci_over_paid"
                },
                {
                    "title": "Adjustment",
                    "payload": "/aci_adjustment"
                }
            ]
        elif csi_category_code == "8":
            text_1 = "8. Statement for Adjustment"
            button_resp_1 = [
                {
                    "title": "Adjustment",
                    "payload": "/aci_adjustment"
                }
            ]
            text_2 = "Alternatively,  would you may also like to fetch one of the following."
            button_resp_2 = [
                {
                    "title": "Over Paid",
                    "payload": "/aci_over_paid"
                },
                {
                    "title": "Partially Paid",
                    "payload": "/aci_partially_paid"
                }
            ]

        dispatcher.utter_message(text=text_1, buttons=button_resp_1)
        dispatcher.utter_message(text=text_2, buttons=button_resp_2)

        return []


# Custom Action - CSI Set Category Code [Route - 1]
# Sets a code for the inquiry type\category
class ActionCSISetCategoryCode(Action):
    def name(self) -> Text:
        return "action_csi_set_category_code"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        CODES = {
            "rri_codes_payment": "2",
            "rri_codes_preauthorization": "3",
            "rri_codes_pbi": "4",
            "rri_codes_admin": "5",
            "aci_codes_over_paid": "6",
            "aci_codes_partially_paid": "7",
            "aci_codes_adjustment": "8"
        }

        print("In action_csi_set_category_code")

        intent = tracker.latest_message['intent'].get('name')
        print(f"intent:{intent}")
        csi_category_code = CODES[intent]
        print(f"csi_category_code: {csi_category_code}")

        return [SlotSet("csi_category_code", csi_category_code)]

# Custom Action - CSI More Details Route - 1
# Makes an API call and gets more details for approved/rejected claim
class ActionCSIMoreDetailsR1(Action):
    def name(self) -> Text:
        return "action_csi_fetch_more_details_r1"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("In action_csi_fetch_more_details_r1 [CSI More Details - Route 1]")

        claim_id = tracker.get_slot('claim_id')
        provider_first_name = tracker.get_slot('provider_first_name')
        provider_last_name = tracker.get_slot('provider_last_name')
        provider_npi = tracker.get_slot('provider_npi')

        # Checking in local DB
        csi_category_code = tracker.get_slot('csi_category_code')
        print(f"csi_category_code: {csi_category_code}, data_type: {type(csi_category_code)}")
        result, existing_details = check_local_db( claim_id, provider_npi, int(csi_category_code))  # check csi_category_code = int/string

        if result == 0:
            fresh_request = 1  # 1: API Call to Payer System
        elif result == 1:
            fresh_request = 0  # 0: API Call to Local DB

        api = CSIMoreDetailsAPI()
        result, more_details = api.get_more_details(claim_id, provider_first_name, provider_last_name, provider_npi, fresh_request, csi_category_code)

        if result == 0:
            dispatcher.utter_message(text="Error in API Call")
        else:
            dispatcher.utter_message(more_details)

            #After prototype, optimize to use action_store_user_details 
            store_user_details(provider_first_name, provider_last_name, provider_npi, claim_id, int(csi_category_code))
            
        return []

# ---------------------------------------------------------- NOT IN HC-PROTOTYPE ----------------------------------------------------------------------

# Custom Action - CSI More Details Set Code [Route - 2]
# Maps the reject reason intent to it's respective code
class ActionSetSubCategoryCode(Action):
    def name(self) -> Text:
        return "action_csi_set_sub_category_code"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        CODES = {
            "rri_payment_denied_charge": "585",
            "rri_payment_procedure_code": "454",
            "rri_payment_combined_procedure_codes": "12",
            "rri_preauthorization_": "",
            "rri_patient_benefits_": "",
            "rri_admin_": "",
            "aci_over_paid_": " ",
            "aci_partially_paid_": " ",
            "aci_adjustment_": " ",
        }

        print("In action_csi_set_sub_category_code")

        intent = tracker.latest_message['intent'].get('name')
        print(f"intent:{intent}")
        csi_sub_category_code = CODES[intent]
        print(f"csi_sub_category_code:{csi_sub_category_code}")
        return [SlotSet("csi_sub_category_code", csi_sub_category_code)]

# Custom Action - CSI More Details Route-2
# Makes an API call and gets more details for reject reason.
class ActionCSIMoreDetailsR2(Action):
    def name(self) -> Text:
        return "action_csi_fetch_more_details_r2"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("In action_csi_fetch_more_details_r1 [CSI More Details - Route 1]")
        claim_id = tracker.get_slot('claim_id')
        provider_first_name = tracker.get_slot('provider_first_name')
        provider_last_name = tracker.get_slot('provider_last_name')
        provider_npi = tracker.get_slot('provider_npi')
        
        # Local DB Check
        # 0: API Call to Local DB; 1: Payer System
        fresh_request = tracker.get_slot('fresh_request')

        api = ClaimStatusInquiryAPI()
        rsc, reject_reason, result = api.get_claim_status(
            claim_id, provider_first_name, provider_last_name, provider_npi, fresh_request)
        if result == 0:
            dispatcher.utter_message(text="Error in API Call")
            return[]

        # Validate User's Reject Reason and the actual Reject Reason
        rri_code = tracker.get_slot('rri_code')
        print(f'rri_code:{rri_code} rsc:{rsc}')

        if rri_code != rsc:
            # Get statement from Venkat
            dispatcher.utter_message(
                "There is a mismatch in the reject reason")

        # Local DB Check
        csi_more_details_code = tracker.get_slot('csi_more_details_code')

        if csi_more_details_code is not None:
            db_check_type = 1
        else:
            api = ClaimStatusInquiryAPI()
            # gets db_check_type code for inquiry type
            db_check_type = api.get_db_check_type(csi_more_details_code)

        api = CSIMoreDetailsAPI()
        result = api.get_more_details(
            claim_id, provider_first_name. provider_last_name, provider_npi, fresh_request)
        # dispatcher.utter_message(result)
        dispatcher.utter_message(text="<-- More Details from API Call -->")
        # if result == 0:
        #     dispatcher.utter_message(text="Error in API Call")
        # else:
        #     dispatcher.utter_message(result)

        return []

# ---------------------------------------------------------- NOT IN HC-PROTOTYPE ----------------------------------------------------------------------

class ActionSetFormSlotsNull(Action):
    def name(self) -> Text:
        return "action_set_form_slots_null"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("claim_id", None), SlotSet("fresh_request", None), SlotSet("exist_in_DB", None),
                SlotSet("request_recency", None), SlotSet("request_recency", None), SlotSet("rri_code", None)]

# Storing user details in DB - need to change according to new schema
class ActionStoreUserDetails(Action):
    """Stores user details in database"""

    def name(self) -> Text:
        return "action_store_user_details"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Storing User details")
        providerFirstName = tracker.get_slot('provider_first_name')
        providerLastName = tracker.get_slot('provider_last_name')
        providerNpi = tracker.get_slot('provider_npi')
        claimId = tracker.get_slot('claim_id')
        print("updating to local DB")

        store_user_details(providerFirstName, providerLastName, providerNpi, claimId, 1)

        return []

# class to explain the form
class ActionExplainForm(Action):
    """Returns the explanation for the form questions"""

    def name(self) -> Text:
        return "action_explain_form"

    def run(self, dispatcher, tracker, domain) -> Text:
        requested_slot = tracker.get_slot("requested_slot")
        print(f"Explaining requested_slot:{requested_slot}")
        # if requested_slot not in CSIDBCheckForm.required_slots(tracker):
        #     print(f"requested slot not in CSIDBCheckForm")
        #     dispatcher.utter_message(
        #         template="Sorry, I didn't get that. Please rephrase or answer the question above."
        #     )
        #     return []
        dispatcher.utter_message(template=f"utter_explain_{requested_slot}")
        return []

# Action - Greet
class ActionGreetUser(Action):
    """Greets the user with/without user's name"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain) -> Text:
        # returns name of latest intent.
        # intent = tracker.latest_message["intent"].get("name")
        # name_entity = next(tracker.get_latest_entity_values("name"), None)
        # if intent == "greet" or (intent == "inform" and name_entity):
        #     if name_entity:
        #         # print("greet with name")
        #         dispatcher.utter_message(
        #             template="utter_greet_name", name=name_entity)
        #         return []
        #     else:
        #         # print("greet without name")
        #         dispatcher.utter_message(template="utter_greet")
        #         return []
        #     return []
        dispatcher.utter_message(template="utter_greet")
        return []