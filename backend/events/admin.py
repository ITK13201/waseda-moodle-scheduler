from django.contrib import admin

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
    list_display = ("id", "event", "user", "status")
    ordering = ("status",)
    fields = ("event", "user", "status")


admin.site.register(Event, EventAdmin)
admin.site.register(EventProgress, EventProgressAdmin)
