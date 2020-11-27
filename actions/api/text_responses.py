CLAIM_TEXT_RESPONSES = {
    "A1": {
        "19": r"""text = f'Yeah! Your claim <b>{user_values["claim_id"]}</b> has been acknowledged as received as of <b>{api_values["lastUpdated"]}</b> and is yet to be accepted for adjudication.'"""},
    "A2": {
        "20": r"""text = f'Yay! your claim is been accepted into adjudication system for processing as of <b>{api_values["lastUpdated"]}</b>. Processing generally takes between 3-7 days.'"""},
    "A4": {
        "35": r"""text = f'Ho no! the details pertaining to Claim ID entered is not found in our records as of <b>{api_values["lastUpdated"]}</b>. Kindly enter a valid claim ID'"""},
    "A7": {
        "0": r"""text = f'Oops! The claim <b>{user_values["claim_id"]}</b> was rejected due to incorrect/ mismatched details as of <b>{api_values["lastUpdated"]}</b>. Dont worry! you can submit a new claim, ensure details are entered correctly'"""},
    "F1": {
        "65": r"""text = f'Hurray! Your claim got approved.\nClaim ID: <b>{user_values["claim_id"]}</b>\nDate of Service: <b>{api_values["claimServiceDate"]}</b>\nTotal claim charge amount: <b>{api_values["totalClaimChargeAmount"]}</b>\nClaim Payment Amount: <b>{api_values["claimPaymentAmount"]}</b>\nPayment Date: <b>{api_values["claimPaymentDate"]}</b>\nComments: <b>"Claim has completed processing and has been paid"</b> as of <b>{api_values["lastUpdated"]}</b>'"""},
    "F2": {
        "585": r"""text = f'Oops! The claim was rejected.\nClaim ID: <b>{user_values["claim_id"]}</b>\nDate of Service: <b>{api_values["claimServiceDate"]}</b>\nTotal claim charge amount: <b>{api_values["totalClaimChargeAmount"]}</b>\nAdjudication Date: <b>{api_values["claimAdjudicationDate"]}</b>\nComments: <b>"Claim has completed processing and was denied charge or Non-covered charge."</b>'"""},
    "F3": {
        "101": r"""text = f'Claim was processed as adjustment to previous claim as of <b>{api_values["lastUpdated"]}</b>'"""},
    "E1": {
        "484": r"""text = f'Response is taking longer time than expected, please try after sometime'"""},
    "P1": {
        "20": r"""text = f'Hola! Claim <b>{user_values["claim_id"]}</b> has been accepted into the adjudication system for processing for Service dated: <b>{api_values["claimServiceDate"]}</b> as of <b>{api_values["lastUpdated"]}</b>.\nProcessing could take 2-4 days working days.'"""}
}