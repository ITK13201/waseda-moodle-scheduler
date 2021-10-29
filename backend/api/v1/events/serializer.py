from rest_framework import serializers
import datetime
import pytz
from dateutil import tz

from django.core.validators import RegexValidator

ORDER_VALIDATOR = RegexValidator(
    regex="(ASC|DESC)", message="Order param must be ASC or DESC."
)
REPLACED_VALUES_WITH_QUERY = {
    "subject": "subject__icontains",
    "title": "title__icontains",
    "from_deadline": "begin_at__gte",
    "to_deadline": "begin_at__lte",
}
JST = tz.gettz("Asia/Tokyo")
UTC = tz.gettz("UTC")

# sample query
# /api/v1/events?title=hoge&subject=hoge&from_deadline=YYYYMMDD&to_deadline=YYYYMMDD&order=ASC&limit=100
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

    def queries(self, data):
        for old_key, new_key in REPLACED_VALUES_WITH_QUERY.items():
            self._change_dict_key(data, old_key, new_key)
        return data

    def _change_dict_key(self, d: dict, old_key: str, new_key: str, default_value=None):
        value = d.pop(old_key, default_value)
        if value is not None:
            d[new_key] = value
