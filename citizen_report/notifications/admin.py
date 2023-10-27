from django.contrib import admin

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "sent_at", "is_read")
    list_filter = ("message", "sent_at")
    search_fields = ("message",)
    ordering = ("sent_at", "is_read")


admin.site.register(Notification, NotificationAdmin)

