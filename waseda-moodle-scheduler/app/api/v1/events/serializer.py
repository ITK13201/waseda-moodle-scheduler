import logging
from copy import deepcopy

from django.core.validators import RegexValidator
from django.db.models import QuerySet
from rest_framework import serializers

from app.events.models import Event

ORDER_VALIDATOR = RegexValidator(
    regex="(ASC|DESC)", message="Order param must be ASC or DESC."
)
REPLACED_VALUES_WITH_QUERY = {
    "subject": "subject__icontains",
    "title": "title__icontains",
    "from_deadline": "begin_at__gte",
    "to_deadline": "begin_at__lte",
}

logger = logging.getLogger(__name__)


# sample query
# GET /api/v1/events/?title=hoge&subject=hoge&from_deadline=YYYYMMDD&to_deadline=YYYYMMDD&order=ASC&limit=100
class EventsApiSerializer(serializers.Serializer):
    subject = serializers.CharField(label="科目名", max_length=200, required=False)
    title = serializers.CharField(label="タイトル", max_length=200, required=False)
    from_deadline = serializers.DateTimeField(
        label="from-開始日時",
        input_formats=[
            "%Y%m%d",
        ],
        required=False,
    )
    to_deadline = serializers.DateTimeField(
        label="to-開始日時",
        input_formats=[
            "%Y%m%d",
        ],
        required=False,
    )
    order = serializers.CharField(
        label="昇順/降順", default="DESC", validators=[ORDER_VALIDATOR], required=False
    )
    limit = serializers.IntegerField(label="表示件数上限", default=10, required=False)

    def validate(self, data: dict):
        # require subject or title
        if data.get("subject") is None and data.get("title") is None:
            raise serializers.ValidationError(
                'Must be required "subject" or "title" field.'
            )
        return data

    def search(self) -> QuerySet[Event]:
        validated_data = deepcopy(self.validated_data)
        logger.info(validated_data)
        limit = validated_data.pop("limit")
        order = validated_data.pop("order")

        queries = self._queries(validated_data)

        if order == "ASC":
            events = Event.objects.filter(**queries).order_by("subject", "title")[
                :limit
            ]
        else:
            events = Event.objects.filter(**queries).order_by("-subject", "-title")[
                :limit
            ]

        return events

    def _queries(self, data):
        for old_key, new_key in REPLACED_VALUES_WITH_QUERY.items():
            self._change_dict_key(data, old_key, new_key)
        return data

    def _change_dict_key(self, d: dict, old_key: str, new_key: str, default_value=None):
        value = d.pop(old_key, default_value)
        if value is not None:
            d[new_key] = value
