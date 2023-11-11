from datetime import datetime

def parse_request(subject_line, body_text):
    if subject_line.find("Community Advisory") != -1:
        print("Community Advisory detected, no action required")
        return
    elif subject_line.find("UC Berkeley WarnMe") != -1:
        print("WarnMe detected, issue time-sensitive push notification")
        return

    body_text = body_text.replace("\r\n\r\n", " ")
    body_text = body_text.replace("\r\n", " ")

    start_ind = body_text.find("On")

    date_time = body_text[start_ind + 3:body_text.find(",")]
    date_time_obj = datetime.strptime(date_time, "%m-%d-%Y %H:%M:%S")

    location_ind = body_text.find(" at ")
    location = body_text[location_ind + 4:body_text.find(".", location_ind)]

    crime_start_ind_1 = body_text.find(" a ")
    crime_start_ind_2 = body_text.find(" an ")
    crime_end_ind = body_text.find(" occurred ")

    if (crime_start_ind_1 < location_ind):
        crime = body_text[crime_start_ind_1 + 3:crime_end_ind]
    elif (crime_start_ind_2 < location_ind):
        crime = body_text[crime_start_ind_2 + 4:crime_end_ind]
    else:
        crime = None

    detail_start_ind = body_text.find(".", location_ind)
    detail_end_ind = body_text.find(" *", detail_start_ind)
    detail = body_text[detail_start_ind + 2:detail_end_ind]

    print(date_time_obj)
    print(location)
    print(crime)
    print(detail)

    return {
        "date_time": date_time_obj,
        "location": location,
        "crime": crime,
        "detail": detail
    }