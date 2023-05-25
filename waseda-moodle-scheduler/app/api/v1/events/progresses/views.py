import logging
from typing import List

from django.forms.models import model_to_dict
from rest_framework import authentication, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.models import EventProgressesQuerySet
from app.usecases.utils import convert_datetime_timezone

from .serializer import (
    EventProgressesApiDELETESerializer,
    EventProgressesApiGETSerializer,
    EventProgressesApiPOSTSerializer,
)

logger = logging.getLogger(__name__)


class EventProgressesAPIView(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request) -> Response:
        params = request.query_params.dict()

        serializer = EventProgressesApiGETSerializer(data=params)
        if serializer.is_valid():
            progresses = serializer.search()
            dataset = self._format_dataset(progresses=progresses)

            return Response(
                dataset,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _format_dataset(self, progresses: EventProgressesQuerySet) -> List[dict]:
        dataset = []
        for progress in progresses:
            data = {}
            data["id"] = progress.id
            data["event"] = model_to_dict(progress.event)
            data["status"] = progress.status
            dataset.append(data)

        for i, data in enumerate(dataset):
            dataset[i] = convert_datetime_timezone(data)

        return dataset

    def post(self, request: Request) -> Response:
        data = request.data

        serializer = EventProgressesApiPOSTSerializer(data=data)
        if serializer.is_valid():
            progress = serializer.save()

            return Response(
                dict(
                    username=progress.user.username,
                    uid=progress.event.uid,
                    status=progress.status,
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        params = request.query_params.dict()

        serializer = EventProgressesApiDELETESerializer(data=params)
        if serializer.is_valid():
            progress = serializer.delete()

            return Response(
                dict(username=progress.user.username, uid=progress.event.uid),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
