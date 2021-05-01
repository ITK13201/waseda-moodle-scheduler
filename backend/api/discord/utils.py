PREVIOUS_TEXT = {
    "new": "課題が**追加**されました．",
    "update": "課題が**更新**されました．",
    "notify": "課題の**締め切り**まであと3日です．",
}
COLOR = {"new": 0x55C500, "update": 0xD85311, "notify": 0xFF69B4}
ICON_PATH = {
    "webhook": "https://raw.githubusercontent.com/ITK13201/waseda-moodle-scheduler/master/static/webhook.png",
    "subject": "https://raw.githubusercontent.com/ITK13201/waseda-moodle-scheduler/master/static/subject.png",
    "calendar": "https://raw.githubusercontent.com/ITK13201/waseda-moodle-scheduler/master/static/calendar.png",
}


def get_embed_contents(event: dict, mode: str) -> dict:
    subject = event["subject"]
    title = event["title"]
    description = event["description"]
    begin_at = event["begin_at"]

    contents = {
        "author": {
            "name": subject,
            "icon_url": ICON_PATH["subject"],
        },
        "title": title,
        "description": description,
        "timestamp": str(begin_at),
        "footer": {"text": "締め切り", "icon_url": ICON_PATH["calendar"]},
        "color": COLOR[mode],
    }

    return contents
