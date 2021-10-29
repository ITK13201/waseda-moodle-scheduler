import requests
import json
from django.conf import settings

from .utils import PREVIOUS_TEXT, get_embed_contents
from backend.usecases.github.subjects import get_subjects

DISCORD_BOT_TOKEN = settings.DISCORD_BOT_TOKEN
SUBJECTS = get_subjects()


def send_notification(event: dict, mode: str):
    subject = event["subject"]
    url = "https://discordapp.com/api/channels/{}/messages".format(SUBJECTS["others"])
    for key, value in SUBJECTS.items():
        if subject == key:
            url = "https://discordapp.com/api/channels/{}/messages".format(value)

    main_content = {
        "content": PREVIOUS_TEXT[mode],
        "embed": get_embed_contents(event, mode),
    }

    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json",
    }

    requests.post(url, json.dumps(main_content), headers=headers)

    print(main_content)
