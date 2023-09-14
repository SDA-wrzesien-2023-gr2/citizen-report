from django.db import models
from django.conf import settings

from .constants import Category, Status


class Report(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reports', on_delete=models.CASCADE)
    clerk = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_reports', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} | {self.created_at}'