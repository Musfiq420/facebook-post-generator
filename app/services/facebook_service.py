import requests
import os
from app.config import GRAPH_VERSION, FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN

def post_to_facebook(message: str):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{FACEBOOK_PAGE_ID}/feed"

    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Facebook API Error: {response.text}")

    return response.json()
