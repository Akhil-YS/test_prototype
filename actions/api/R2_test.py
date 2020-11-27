def get_category(code):
  # rri_codes_payment = ["585", "454", "12"]
  rri_codes_payment=["103", "475", "488", "86", "454","596", "474", "585", "764"] # csi rejected claim - payment related codes
  rri_codes_preauthorization = ["84", "91", "674"] # csi rejected claim - preauthorization related codes
  rri_codes_pbi = ["81", "780"] # csi rejected claim - patient benefits related codes
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

get_category("764")