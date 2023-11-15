import dotenv
dotenv.load_dotenv()

from firebase_functions import https_fn
from firebase_admin import initialize_app
from firebase_admin import firestore
import requests
import os
import parse

debug = bool(os.environ.get("DEBUG"))
debug_url = os.environ.get("DEBUG_URL")

initialize_app()

@https_fn.on_request()
def safety_process(request: https_fn.Request) -> https_fn.Response:
    request_json = request.get_json(silent=True)

    if debug:
        requests.post(debug_url, json=request_json)

    subject_line = request_json["payload"]["Subject"]
    body_text = request_json["payload"]["stripped-text"]

    parsed = parse.parse_request(subject_line, body_text)

    if parsed:
        db = firestore.client()
        db.collection("Safety Logs").document(str(parsed["date_time"])).set(parsed)

    return https_fn.Response(str(request.data))