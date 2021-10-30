from rest_framework import serializers
import datetime
import pytz
from dateutil import tz

from django.core.validators import RegexValidator

from backend.users.models import User
from backend.events.models import STATUS_CHOICES

ORDER_VALIDATOR = RegexValidator(
    regex="(ASC|DESC)", message="Order param must be ASC or DESC."
)
REPLACED_VALUES_WITH_QUERY = {
    "username": "user__username",
    "subject": "event__subject__icontains",
    "title": "event__title__icontains",
    "from_deadline": "event__begin_at__gte",
    "to_deadline": "event__begin_at__lte",
    "status": "status",
}
JST = tz.gettz("Asia/Tokyo")
UTC = tz.gettz("UTC")

# sample query
# GET /api/v1/events/progresses?username=taro&title=hoge&subject=hoge&from_deadline=YYYYMMDD&to_deadline=YYYYMMDD&order=ASC&limit=100
class EventProgressesApiSerializer(serializers.Serializer):
    username = serializers.CharField(label="ユーザ名", max_length=200, required=True)
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
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    order = serializers.CharField(
        label="昇順/降順", default="DESC", validators=[ORDER_VALIDATOR], required=False
    )
    limit = serializers.IntegerField(label="表示件数上限", default=10, required=False)

    def validate_username(self, data: str):
        if data:
            try:
                User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User whose this username Not Found.")

        return data

    def queries(self, data):
        for old_key, new_key in REPLACED_VALUES_WITH_QUERY.items():
            self._change_dict_key(data, old_key, new_key)
        return data

    def _change_dict_key(self, d: dict, old_key: str, new_key: str, default_value=None):
        value = d.pop(old_key, default_value)
        if value is not None:
            d[new_key] = value
