import datetime
import logging

from dateutil.tz import gettz
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from rest_framework.request import Request

from .serializer import EventsApiSerializer
from backend.events.models import Event


logger = logging.getLogger(__name__)


class EventsAPIView(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request):
        params = request.query_params.dict()

        serializer = EventsApiSerializer(data=params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            logger.info(validated_data)
            limit = validated_data.pop("limit")
            order = validated_data.pop("order")

            queries = serializer.queries(validated_data)

            if order == "ASC":
                events = Event.objects.filter(**queries).order_by("subject", "title")[
                    :limit
                ]
            else:
                events = Event.objects.filter(**queries).order_by("-subject", "-title")[
                    :limit
                ]

            # utc to jst
            data = list(events.values())
            for obj in data:
                for key, value in obj.items():
                    if isinstance(value, datetime.datetime):
                        obj[key] = self._convert_utc_to_jst(value)

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _convert_utc_to_jst(self, dt_utc: datetime.datetime) -> datetime.datetime:
        dt_jst = dt_utc.astimezone(gettz(settings.TIME_ZONE))
        return dt_jst
