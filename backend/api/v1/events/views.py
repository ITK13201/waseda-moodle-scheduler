import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from rest_framework.request import Request

from backend.usecases.utils import convert_datetime_timezone
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
            dataset = list(events.values())
            for i, data in enumerate(dataset):
                dataset[i] = convert_datetime_timezone(data)

            return Response(dataset, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
