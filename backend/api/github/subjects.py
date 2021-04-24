import os

import requests
import json
import base64
from django.conf import settings
from github import Github

GITHUB_ACCESS_TOKEN = settings.GITHUB_ACCESS_TOKEN


def get_subjects() -> dict:
    github = Github(GITHUB_ACCESS_TOKEN)
    repository = github.get_repo("ITK13201/PrivateFiles")
    contents = repository.get_contents("waseda-moodle-scheduler/subject.json")
    content = base64.b64decode(contents.content).decode("utf-8")
    subjects = json.loads(content)

    return subjects
