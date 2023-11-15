"""
geo.py
This file contains functions for geocoding addresses.

"""

import dotenv
dotenv.load_dotenv()

import os
import requests

GOOGLE_API_KEY = os.environ.get("GCLOUD_MAP_API")
ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

def get_request_endpoint(address):
    return f"{ENDPOINT}?address={address}&key={GOOGLE_API_KEY}"


def get_lat_long(address):
    """
    Returns a dictionary of latitude and longitude for a given address.

    Sample output:
        {
            "lat": 37.8718535,
            "lng": -122.258423
        }
    """
    endpoint = get_request_endpoint(address)
    response = requests.get(endpoint)
    if response.status_code != 200:
        return None
    else:
        result = response.json()
        if result["status"] == "ZERO_RESULTS":
            return None
        return result["results"][0]["geometry"]["location"]