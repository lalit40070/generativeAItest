import requests
from app.core.config import get_app_settings

async def post_to_firebase(
        fcm_token: str,
        title: str,
        body: str
    ) -> int:
    """Posts content to firebase"""

    settings = get_app_settings()

    body = {
        "to": fcm_token,
        "notification": {"body": body, "title": title, "mutable_content": False}
    }

    headers = {"Authorization": "key=" + settings.firebase_key, "Content-Type" : settings.firebase_content_type}
    response = requests.post(settings.firebase_url, json=body, headers=headers)
    # ! Should log response body here
    return response.status_code