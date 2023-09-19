from django.contrib.auth import get_user_model
from django.db import models

from report.models import Report

User = get_user_model()


class NewsPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    created_at = models.DateField()
    image = models.ImageField(upload_to='images/', blank=True)
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='report_posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.title} | {self.created_at}'
