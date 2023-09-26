from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from .constants import Category, Status

User = settings.AUTH_USER_MODEL


class Report(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    clerk = models.ForeignKey(User, related_name='assigned_reports', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.title} | {self.updated_at}'
