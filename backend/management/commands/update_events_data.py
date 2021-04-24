import os
import ics
import traceback
import requests
from django.core.management.base import BaseCommand

from backend.events.models import Event
from backend.api.discord import webhook


MOODLE_CALENDAR_URL = os.environ.get("MOODLE_CALENDAR_URL")


class Command(BaseCommand):
    help = "Update events data"

    def handle(self, *args, **options):

        try:
            self.update_events()
        except Exception as err:
            traceback.print_exc()
            self.stdout.write(self.style.ERROR("Failed updating events data"))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully updating events data"))

    def update_events(self):
        events = self._get_events()
        for event in events:
            try:
                model = Event.objects.get(uid=event["uid"])
                model_exists = True
            except Event.DoesNotExist:
                model_exists = False

            if model_exists:
                if not model.last_modified_at == event["last_modified_at"]:
                    model.title = event["title"]
                    model.description = event["description"]
                    model.begin_at = event["begin_at"]
                    model.end_at = event["end_at"]
                    model.last_modified_at = event["last_modified_at"]
                    model.save()

                    webhook.send_notification(event=event, mode="update")
            else:
                model = Event(
                    uid=event["uid"],
                    subject=event["subject"],
                    title=event["title"],
                    description=event["description"],
                    begin_at=event["begin_at"],
                    end_at=event["end_at"],
                    last_modified_at=event["last_modified_at"],
                )
                model.save()

                webhook.send_notification(event=event, mode="new")

    def _get_events(self) -> list:
        response = requests.get(MOODLE_CALENDAR_URL)
        calendar = ics.Calendar(response.text)

        events = list(calendar.timeline)

        events_list = []
        for event in events:
            event_dict = {
                "uid": event.uid,
                "subject": event.categories.pop(),
                "title": event.name,
                "description": event.description,
                "begin_at": event.begin.datetime,
                "end_at": event.end.datetime,
                "last_modified_at": event.last_modified.datetime,
            }
            events_list.append(event_dict)

        return events_list
