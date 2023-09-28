from django.contrib import admin

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "category")
    ordering = ("title",)


admin.site.register(Report, ReportAdmin)
