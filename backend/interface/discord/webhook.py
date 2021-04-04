import os
import requests
import json
from django.templatetags.static import static

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

PREVIOUS_TEXT = {"new": "課題が**追加**されました．", "update": "課題が**更新**されました．"}
COLOR = {"new": 5620992, "update": 14177041}


def send_notification(event: dict, mode: str):

    webhook_url = DISCORD_WEBHOOK_URL

    main_content = {
        "username": "task scheduler",
        "avatar_url": static("webhook.png"),
        "content": PREVIOUS_TEXT[mode],
        "embeds": [_get_contents_infomation(event, mode)],
    }

    requests.post(
        webhook_url, json.dumps(main_content), headers={"Content-Type": "application/json"}
    )


def _get_contents_infomation(event: dict, mode: str) -> dict:
    subject = event["subject"]
    title = event["title"]
    description = event["description"]
    begin_at = event["begin_at"]

    infomation = {
        "author": {
            "name": subject,
            "icon_url": static("subject.png"),
        },
        "title": title,
        "description": description,
        "timestamp": str(begin_at),
        "footer": {"text": "締め切り: ", "icon_url": static("calendar.png")},
        "color": COLOR[mode],
    }

    return infomation
