from datetime import datetime
from geo import get_lat_long

def parse_request(subject_line, body_text):
    if subject_line.find("Community Advisory") != -1:
        print("Community Advisory detected, no action required")
        return
    elif subject_line.find("UC Berkeley WarnMe") != -1:
        print("WarnMe detected, issue time-sensitive push notification")
        return

    body_text = body_text.replace("\r\n\r\n", " ")
    body_text = body_text.replace("\r\n", " ")
    body_text = body_text.replace("\n", " ")

    start_ind = body_text.find("On")

    date_time = body_text[start_ind + 3:body_text.find(",")]
    date_time_obj = datetime.strptime(date_time, "%m-%d-%Y %H:%M:%S")

    location_ind = body_text.find(" at ")
    location = body_text[location_ind + 4:body_text.find(".", location_ind)].strip()

    crime_start_ind_1 = body_text.find(" a ")
    crime_start_ind_2 = body_text.find(" an ")
    crime_end_ind = body_text.find(" occurred ")

    if (crime_start_ind_1 < location_ind):
        crime = body_text[crime_start_ind_1 + 3:crime_end_ind].strip()
    elif (crime_start_ind_2 < location_ind):
        crime = body_text[crime_start_ind_2 + 4:crime_end_ind].strip()
    else:
        crime = None

    detail_start_ind = body_text.find(".", location_ind)
    detail_end_ind_1 = body_text.find("If you have", detail_start_ind)
    detail_end_ind_2 = body_text.find("*", detail_start_ind)
    detail_end_ind = min(detail_end_ind_1, detail_end_ind_2)
    detail = body_text[detail_start_ind + 2:detail_end_ind].strip()

    print(date_time_obj)
    print(location)
    print(crime)
    print(detail)

    # Create dictionary to be uploaded to Firebase
    firebase_obj = {
        "date_time": date_time_obj,
        "location": location,
        "crime": crime,
        "detail": detail
    }

    # Use geo.py Google Geocoding API to get latitude and longitude, if it exists
    lat_long = get_lat_long(f"{location} Berkeley CA")
    if lat_long:    # if lat_long is not None
        firebase_obj["latitude"] = lat_long["lat"]
        firebase_obj["longitude"] = lat_long["lng"]
    
    return firebase_obj