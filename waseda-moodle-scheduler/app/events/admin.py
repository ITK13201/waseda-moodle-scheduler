from django.contrib import admin
from django.urls import reverse

from .models import Event, EventProgress


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "subject",
        "title",
        "description",
        "begin_at",
        "end_at",
        "last_modified_at",
        "notified_at",
    )
    ordering = ("-begin_at",)
    fields = (
        "uid",
        "subject",
        "title",
        "description",
        "begin_at",
        "end_at",
        "last_modified_at",
        "notified_at",
    )


class EventProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "event", "subject", "title", "description")
    ordering = ("user", "status",)
    fields = ("event", "user", "status")

    def subject(self, obj: EventProgress):
        return obj.event.subject
    
    def title(self, obj: EventProgress):
        return obj.event.title
    
    def description(self, obj: EventProgress):
        return obj.event.description
    
    subject.short_description = "科目名"
    title.short_description = "タイトル"
    description.short_description = "説明"


admin.site.register(Event, EventAdmin)
admin.site.register(EventProgress, EventProgressAdmin)
