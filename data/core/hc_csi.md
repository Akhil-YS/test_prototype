## main options
* home
  - utter_welcome_message_1
  - utter_welcome_help

## restart chat
* restart_conversation
  - utter_welcome_message_1
  - utter_welcome_help
  - action_restart

<!-- Claim Status Inquiry(CSI) - conversation flows - 4 scenarios -->
<!-- CSI-(4 scenarios) starts here -->
## claim_status + in DB + <12hrs
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - slot{"claim_id": null}
  - slot{"fresh_request": null}
  - slot{"exist_in_DB": null}
  - slot{"request_recency": null}
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
  - form{"name": null}
  - action_db_check
  - slot{"exist_in_DB": "yes"}
  - slot{"request_recency": "recent"}
  - utter_processing
  - action_csi_fetch
  - slot{"request_recency": "recent"}  
  - slot{"csi_more_details": "no"}
  - utter_csi_anything_else

## claim_status + in DB + >12hrs + refetch
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - slot{"claim_id": null}
  - slot{"fresh_request": null}
  - slot{"exist_in_DB": null}
  - slot{"request_recency": null}
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
  - form{"name": null}
  - action_db_check
  - slot{"exist_in_DB": "yes"}
  - slot{"request_recency": "not_recent"} 
  - utter_processing
  - action_csi_fetch
  - slot{"csi_more_details": "no"}
  - utter_ask_csi_refetch
* affirm_good
  - utter_processing
  - action_csi_refetch
  - slot{"csi_more_details": "no"}
  - action_store_user_details
  - slot{"csi_more_details": "no"}
  - utter_csi_anything_else

## claim_status + in DB + >12hrs + no_refetch
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - slot{"claim_id": null}
  - slot{"fresh_request": null}
  - slot{"exist_in_DB": null}
  - slot{"request_recency": null}
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
  - form{"name": null}
  - action_db_check
  - slot{"exist_in_DB": "yes"}
  - slot{"request_recency": "not_recent"}
  - utter_processing
  - action_csi_fetch
  - slot{"csi_more_details": "no"}
  - utter_ask_csi_refetch
* deny 
  - slot{"csi_more_details": "no"}
  - utter_csi_anything_else  

<!-- If not in DB -->
## claim_status + not in DB
* claim_status_inquiry
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - slot{"claim_id": null}
  - slot{"fresh_request": null}
  - slot{"exist_in_DB": null}
  - slot{"request_recency": null}
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
  - form{"name": null}
  - action_db_check
  - slot{"exist_in_DB": "no"}
  - csi_provider_names_form
  - form{"name": "csi_provider_names_form"}
  - form{"name": null}
  - utter_processing
  - action_csi_fetch
  - slot{"csi_more_details": "no"}
  - action_store_user_details
  - utter_csi_anything_else
<!-- CSI-(4 scenarios) ends here -->