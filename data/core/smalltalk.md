## smalltalk
* smalltalk 
   - respond_smalltalk
   - utter_anything_else

## smalltalk
* smalltalk 
   - respond_smalltalk
   - utter_anything_else
* smalltalk 
   - respond_smalltalk
   - utter_anything_else

## greet -> small talk
* greet
   - action_greet_user
* smalltalk
   - respond_smalltalk
   - utter_anything_else

## greet -> small talk -> smalltalk
* greet
   - action_greet_user
* smalltalk
   - respond_smalltalk
   - utter_anything_else
* smalltalk
   - respond_smalltalk
   - utter_anything_else

## greet -> chitchat -> form -> anything else
* greet
   - action_greet_user
* smalltalk
   - respond_smalltalk
   - utter_anything_else
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null

## greet -> chitchat -> form -> anything else
* greet
   - action_greet_user
* smalltalk
   - respond_smalltalk
   - utter_anything_else
* smalltalk
   - respond_smalltalk
   - utter_anything_else
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null

<!-- Small Talks with Claim Status Inquiry(CSI) -->
<!-- ## greet -> form, chitchat -> continue ->form -> anything else
* claim_status_inquiry
   - utter_can_do
   - utter_details_message
   - form{"name": null}
   - action_set_form_slots_null
   - csi_db_check_form
   - form{"name": "csi_db_check_form"}
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* affirm_good
   - utter_great
   - csi_db_check_form
   - form{"name": null}

## greet -> form, chitchat -> continue ->form -> anything else
* claim_status_inquiry
   - utter_can_do
   - utter_details_message
   - form{"name": null}
   - action_set_form_slots_null
   - csi_db_check_form
   - form{"name": "csi_db_check_form"}
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* affirm_good
   - utter_great
   - csi_db_check_form
   - form{"name": null}


## greet -> form, chitchat -> don't continue -> anything else
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* deny
   - utter_deny
   - action_deactivate_form
   - form{"name": null}
   - utter_deny_anything_else

## greet -> form, chitchat -> don't continue -> anything else
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* smalltalk
   - respond_smalltalk
   - utter_ask_continue_form
* deny
   - utter_deny
   - action_deactivate_form
   - form{"name": null}
   - utter_deny_anything_else -->