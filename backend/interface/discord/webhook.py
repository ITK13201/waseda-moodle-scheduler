import os
import requests

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

PREVIOUS_TEXT = {
    "new": "課題が追加されました．",
    "update": "課題が更新されました．"
}

def send_notification(event: dict, mode: str):

    webhook_url = DISCORD_WEBHOOK_URL
    
    main_content = {
        "username": "task scheduler",
        #"avatar_url": "",
        "content": _get_data_to_update(event, mode)
    }
    
    requests.post(webhook_url, main_content)

def _get_data_to_update(event: dict, mode: str) -> str:
    subject = event["subject"]
    title = event["title"]
    description = event["description"]
    begin_at = event["begin_at"]
    previous_text = PREVIOUS_TEXT[mode]
    
    text = previous_text + "\n" \
        + "```\n" \
        + "科目: " + str(subject) + "\n" \
        + "題名: " + str(title) + "\n" \
        + "説明: " + str(description) + "\n" \
        + "\n" \
        + "締め切り: " + str(begin_at) + "\n" \
        + "```"

    return text
