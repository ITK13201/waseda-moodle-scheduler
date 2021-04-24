import requests
import json
from django.conf import settings

from .utils import PREVIOUS_TEXT, ICON_PATH, get_embed_contents

DISCORD_WEBHOOK_URL = settings.DISCORD_WEBHOOK_URL


def send_notification(event: dict, mode: str):
    webhook_url = DISCORD_WEBHOOK_URL

    main_content = {
        "username": "task scheduler",
        "avatar_url": ICON_PATH["webhook"],
        "content": PREVIOUS_TEXT[mode],
        "embeds": [get_embed_contents(event, mode)],
    }

    requests.post(
        webhook_url, json.dumps(main_content), headers={"Content-Type": "application/json"}
    )
