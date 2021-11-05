import logging

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

logger = logging.getLogger(__name__)

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
                self.user = User.objects.get(username=data)
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
    user: User = None
    event: Event = None

    def validate_username(self, data: str):
        if data:
            try:
                self.user = User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User whose this username Not Found.")

        return data

    def validate_uid(self, data: str):
        if data:
            try:
                self.event = Event.objects.get(uid=data)
            except Event.DoesNotExist:
                raise serializers.ValidationError("Event with this uid Not Found.")

        return data

    def save(self, commit=True) -> EventProgress:
        validated_data = self.validated_data
        progress_status = validated_data["status"]
        logger.info(validated_data)

        progress: EventProgress = None
        if commit:
            try:
                progress = EventProgress.objects.related_other_models().get(
                    event=self.event,
                    user=self.user,
                )
            except EventProgress.DoesNotExist:
                progress = EventProgress(
                    event=self.event,
                    user=self.user,
                )
            finally:
                progress.status = progress_status
                progress.save()

        return progress


# DELETE /api/v1/events/progresses/?username=taro&uid=xxxx@wsdmoodle.waseda.jp
class EventProgressesApiDELETESerializer(serializers.Serializer):
    username = serializers.CharField(label="ユーザ名", max_length=200, required=True)
    uid = serializers.CharField(label="uid", max_length=200, required=True)
    user: User = None
    event: Event = None
    progress: EventProgress = None

    def validate_username(self, data: str):
        if data:
            try:
                self.user = User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User whose this username Not Found.")

        return data

    def validate_uid(self, data: str):
        if data:
            try:
                self.event = Event.objects.get(uid=data)
            except Event.DoesNotExist:
                raise serializers.ValidationError("Event with this uid Not Found.")

        return data

    def validate(self, data: dict):
        if data:
            try:
                self.progress = EventProgress.objects.get(
                    event=self.event, user=self.user
                )
            except EventProgress.DoesNotExist:
                raise serializers.ValidationError(
                    "event progress with this username and uid is Not Found."
                )

        return data
