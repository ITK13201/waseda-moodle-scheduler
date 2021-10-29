from django.urls import path
from django.urls.conf import include

from .events import views as events_views

urlpatterns = [
    path("events/", events_views.EventsAPIView.as_view(), name="api_v1_events")
]
