from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = ((0, "TODO"), (1, "DOING"), (2, "DONE"))


class Event(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.CharField(_("uid"), max_length=100, unique=True)
    subject = models.CharField(_("科目名"), max_length=200)
    title = models.CharField(_("タイトル"), max_length=200)
    description = models.TextField(_("説明"), blank=True, null=True)
    begin_at = models.DateTimeField(_("開始日時"), blank=True, null=True)
    end_at = models.DateTimeField(_("終了日時"), blank=True, null=True)
    last_modified_at = models.DateTimeField(_("更新日時"), blank=True, null=True)
    notified_at = models.DateTimeField(_("通知日時"), blank=True, null=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.uid

    @property
    def dict_type(self):
        return self.__dict__


class EventProgress(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, verbose_name="イベント"
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="ユーザ")
    status = models.IntegerField(
        _("進捗状況"), blank=False, null=False, choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = "EventProgress"
        verbose_name_plural = "EventProgresses"

    def get_status(self) -> str:
        return self.get_status_display()
