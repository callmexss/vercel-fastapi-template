import requests

from app.config import settings


def save_to_memos(content: str):
    url = settings.MEMOS_API_BASE
    headers = {
        "Authorization": f"Bearer {settings.MEMOS_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "content": content,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response
