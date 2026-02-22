import requests
from app.config import GRAPH_VERSION, FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN

def post_to_facebook(message: str, photo_id: str = None):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{FACEBOOK_PAGE_ID}/feed"
    
    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }

    # attach pre-uploaded image if available
    if photo_id:
        payload["attached_media[0]"] = f'{{"media_fbid":"{photo_id}"}}'

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Facebook API Error: {response.text}")
    
    return response.json()