import traceback
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from backend.events.models import Event
from backend.api.discord import bot

DAYS_DIFF = 3
MINUTES_DIFF = 40


class Command(BaseCommand):
    help = "Notify deadline of events"

    def handle(self, *args, **options):
        try:
            self.notify_deadline()
        except Exception:
            traceback.print_exc()
            self.stdout.write(self.style.ERROR("Failed notifying deadline of events"))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully notifying deadline of events"))

    def notify_deadline(self):
        now = timezone.now()
        start = now + timedelta(days=DAYS_DIFF) - timedelta(minutes=MINUTES_DIFF)
        end = now + timedelta(days=DAYS_DIFF, minutes=MINUTES_DIFF)
        events = Event.objects.filter(begin_at__range=(start, end), notified_at__isnull=True)
        for event in events:
            bot.send_notification(event=event.dict_type, mode="notify")
            event.notified_at = now
            event.save()
