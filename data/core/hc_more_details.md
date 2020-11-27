<!-- CSI More Details - 2 Routes -->
<!-- CSI More Details Route-1 starts here -->
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
  - slot{"request_recency":"recent"}  
  - slot{"csi_more_details": "yes"}
  - action_csi_more_details_buttons

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
  - slot{"csi_more_details": "yes"}
  - utter_ask_csi_refetch
* affirm_good
  - utter_processing
  - action_csi_refetch
  - slot{"csi_more_details": "yes"}
  - action_store_user_details
  - slot{"csi_more_details": "yes"}
  - action_csi_more_details_buttons

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
  - slot{"csi_more_details": "yes"}
  - utter_ask_csi_refetch
* deny 
  - slot{"csi_more_details": "yes"}
  - action_csi_more_details_buttons

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
  - action_csi_refetch 
  - slot{"csi_more_details": "yes"}
  - action_store_user_details
  - action_csi_more_details_buttons

## CSI More Details Route - 1
* rri_payment OR rri_preauthorization OR rri_pbi OR aci_over_paid OR aci_partially_paid OR aci_adjustment
  - action_csi_set_category_code
  - slot{"csi_category_code": "2"} 
  - utter_wait_more_details
  - action_csi_fetch_more_details_r1 

<!-- store user details -->

<!-- CSI More Details Route-1 ends here -->

<!-- CSI More Details Route-2 starts here -->

<!-- ## rri_payment 585, 454, 12
* rri_payment_deniedcharge OR rri_payment_procedurecode OR rri_payment_combinedprocedurecodes
  - utter_can_do
  - utter_details_message
  - form{"name": null}
  - action_set_form_slots_null
  - slot{"claim_id": null}
  - slot{"fresh_request": null}
  - slot{"exist_in_DB": null}
  - slot{"request_recency": null}
  - slot{"rri_code": null} 
  - action_rri_set_code
  - csi_db_check_form
  - form{"name": "csi_db_check_form"}
  - form{"name": null}
  - action_db_check
  - slot{"exist_in_DB": "yes"}
  - slot{"request_recency": "recent"}
  - csi_provider_names_form
  - form{"name": "csi_provider_names_form"}
  - form{"name": null}
  - utter_wait_more_details -->
  <!-- write code -->
  <!-- - action_rri_payment2 
  - utter_csi_anything_else   -->

<!-- CSI More Details Route-2 ends here -->