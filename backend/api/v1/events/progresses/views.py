import logging
from typing import List

from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from rest_framework.request import Request

from .serializer import EventProgressesApiSerializer
from backend.events.models import EventProgress, EventProgressesQuerySet
from backend.usecases.utils import convert_datetime_timezone


logger = logging.getLogger(__name__)


class EventProgressesAPIView(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request):
        params = request.query_params.dict()

        serializer = EventProgressesApiSerializer(data=params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            logger.info(validated_data)
            limit = validated_data.pop("limit")
            order = validated_data.pop("order")

            queries = serializer.queries(validated_data)
            if order == "ASC":
                event_progresses = (
                    EventProgress.objects.related_other_models()
                    .filter(**queries)
                    .order_by("status", "event__subject", "event__title")[:limit]
                )
            else:
                event_progresses = (
                    EventProgress.objects.related_other_models()
                    .filter(**queries)
                    .order_by("-status", "-event__subject", "-event__title")[:limit]
                )

            dataset = self._format_dataset(event_progresses=event_progresses)

            return Response(
                dataset,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _format_dataset(self, event_progresses: EventProgressesQuerySet) -> List[dict]:
        dataset = []
        for event_progress in event_progresses:
            data = {}
            data["id"] = event_progress.id
            data["event"] = model_to_dict(event_progress.event)
            data["status"] = event_progress.status
            dataset.append(data)

        for i, data in enumerate(dataset):
            dataset[i] = convert_datetime_timezone(data)

        return dataset
