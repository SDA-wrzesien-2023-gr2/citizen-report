from django.contrib import admin

from .models import NewsPost

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['title', 'text']

admin.site.register(NewsPost, PostAdmin)
