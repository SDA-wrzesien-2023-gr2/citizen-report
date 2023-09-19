from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

Report = 'report.Report'
User = 'authSystem.User'


class Notification(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)


# UNDER CONSTRUCTION:
# @receiver(post_save, sender=Report)
# def create_notification


