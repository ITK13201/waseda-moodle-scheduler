from rest_framework import serializers

from django.core.validators import RegexValidator

from backend.users.models import User
from backend.events.models import STATUS_CHOICES, Event, EventProgress

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

# sample query
# GET /api/v1/events/progresses/?username=taro&title=hoge&subject=hoge&from_deadline=YYYYMMDD&to_deadline=YYYYMMDD&order=ASC&limit=100
class EventProgressesApiGETSerializer(serializers.Serializer):
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
    status = serializers.ChoiceField(
        label="進捗状況", choices=STATUS_CHOICES, required=False
    )
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


# POST /api/v1/events/progresses/ body => [username=taro,uid=xxxx@wsdmoodle.waseda.jp,status=1]
class EventProgressesApiPOSTSerializer(serializers.Serializer):
    username = serializers.CharField(label="ユーザ名", max_length=200, required=True)
    uid = serializers.CharField(label="uid", max_length=200, required=True)
    status = serializers.ChoiceField(
        label="進捗状況", choices=STATUS_CHOICES, default=0, required=False
    )

    def validate_username(self, data: str):
        if data:
            try:
                User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User whose this username Not Found.")

        return data

    def validate_uid(self, data: str):
        if data:
            try:
                Event.objects.get(uid=data)
            except Event.DoesNotExist:
                raise serializers.ValidationError("Event with this uid Not Found.")

        return data


# DELETE /api/v1/events/progresses/?username=taro&uid=xxxx@wsdmoodle.waseda.jp
class EventProgressesApiDELETESerializer(serializers.Serializer):
    username = serializers.CharField(label="ユーザ名", max_length=200, required=True)
    uid = serializers.CharField(label="uid", max_length=200, required=True)

    def validate_username(self, data: str):
        if data:
            try:
                User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User whose this username Not Found.")

        return data

    def validate_uid(self, data: str):
        if data:
            try:
                Event.objects.get(uid=data)
            except Event.DoesNotExist:
                raise serializers.ValidationError("Event with this uid Not Found.")

        return data

    def validate(self, data: dict):
        if data:
            username = data.get("username")
            uid = data.get("uid")

            try:
                user = User.objects.get(username=username)
                event = Event.objects.get(uid=uid)
                EventProgress.objects.get(event=event, user=user)
            except EventProgress.DoesNotExist:
                raise serializers.ValidationError(
                    "event progress with this username and uid is Not Found."
                )

        return data
