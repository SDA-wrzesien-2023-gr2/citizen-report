from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from report.models import Report

User = settings.AUTH_USER_MODEL


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts', limit_choices_to={"is_staff": True})
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='report_posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.title} | {self.created_at}'


class NewsComment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user)