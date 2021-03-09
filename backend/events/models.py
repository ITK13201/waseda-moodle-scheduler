from django.db import models
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uid = models.CharField(_("uid"), max_length=50, unique=True)
    subject = models.CharField(_("科目名"), max_length=50)
    title = models.CharField(_("タイトル"), max_length=50)
    description = models.TextField(_("説明"), blank=True, null=True)
    begin_at = models.DateTimeField(_("開始日時"), blank=True, null=True)
    end_at = models.DateTimeField(_("終了日時"), blank=True, null=True)
    last_modified_at = models.DateTimeField(_("更新日時"), blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Event'

    def __str__(self):
        return f"[{self.subject}]------[{self.title}]"