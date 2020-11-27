## thanks
* thank
    - utter_noworries
    - utter_anything_else
    
## anything else + yes
    - utter_anything_else
* affirm_good
    - utter_affirm_what_help    

## anything else + no
    - utter_anything_else
* deny OR affirm_bad
    - utter_deny
    - utter_conversation_end_text
    - utter_start_new_conversation

## deny_anything_else + yes
    - utter_deny_anything_else
* affirm_good
    - utter_affirm_what_help    

## deny_anything_else + no
    - utter_deny_anything_else
* deny OR affirm_bad
    - utter_deny
    - utter_conversation_end_text
    - utter_start_new_conversation

## what_help? + no 
    - utter_what_help
* deny OR affirm_bad
    - utter_deny
    - utter_conversation_end_text
    - utter_start_new_conversation

## bye
* bye
    - utter_bye
    
## greet
* greet
    - action_greet_user

## greet + hru + positive_response
* greet
    - action_greet_user
* affirm_good
    - utter_user_good
    - utter_what_help

## greet + hru + negative_response [user skipped]
* greet
    - action_greet_user
* affirm_bad OR deny
    - utter_cheer_up
    - utter_did_that_help

## greet + hru + negative_response + helped
* greet
    - action_greet_user
* affirm_bad OR deny
    - utter_cheer_up
    - utter_did_that_help
* affirm_good
    - utter_react_positive    
    - utter_what_help

## greet + hru + negative_response + didn't help
* greet
    - action_greet_user
* affirm_bad OR deny
    - utter_cheer_up
    - utter_did_that_help
* deny OR affirm_bad
    - utter_react_negative    
    - utter_deny_anything_else