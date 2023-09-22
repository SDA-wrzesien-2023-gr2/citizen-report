from django.contrib import admin

from .models import NewsPost, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['title', 'text']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'post', 'created_at', 'approved_comment')
    list_filter = ('approved_comment', 'created_at')
    search_fields = ('name', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)


admin.site.register(NewsPost, PostAdmin)
admin.site.register(Comment, CommentAdmin)
