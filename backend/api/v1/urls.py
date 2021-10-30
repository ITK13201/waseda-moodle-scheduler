from django.urls import path
from django.urls.conf import include

from .events.views import EventsAPIView
from .events.progresses.views import EventProgressesAPIView

urlpatterns = [
    path("events/", EventsAPIView.as_view(), name="api_v1_events"),
    path(
        "events/progresses/",
        EventProgressesAPIView.as_view(),
        name="api_v1_events_progresses",
    ),
]
