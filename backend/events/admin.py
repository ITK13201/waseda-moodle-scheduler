from django.contrib import admin

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uid',
        'subject',
        'title',
        'description',
        'begin_at',
        'end_at',
        'last_modified_at'
    )
    ordering = ('-begin_at',)
    fields = (
        'uid',
        'subject',
        'title',
        'description',
        'begin_at',
        'end_at',
        'last_modified_at'
    )

admin.site.register(Event, EventAdmin)
