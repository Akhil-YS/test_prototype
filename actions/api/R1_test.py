def get_category(rcc, rsc):

    CATEGORY_CODES = {
        "F1": {
            "521": "8",
            "47": "7"},
        "F3": {
            "101": "6"},
        "A2": {
            "3": "1"},
        "P0": {
            "38": "1",
            "44": "1",
            "685": "1",
            "686": "1"},
        "A7": {
            "29": "5",
            "116": "5",
            "475": "2",
            "454": "2"},
        "A4": {
            "33": "5"
        },
        "F2": {
            "81": "4",
            "780": "4",
            "585": "2",
            "84": "3",
            "91": "3",
            "674": "3"}
    }

    return CATEGORY_CODES[rcc][rsc]

rcc = "F2"
rsc = "81"
inquiry_category_code = get_category(rcc, rsc)
print(inquiry_category_code)