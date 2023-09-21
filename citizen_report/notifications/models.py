from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from authSystem.models import  User

Report = 'report.Report'
# User = 'authSystem.User'


class Notification(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


# UNDER CONSTRUCTION:
@receiver(post_save, sender=Report)
def create_notification(sender, created, instance, update_fields, **kwargs):
    message = f'new report {instance.title} added!' if created else f'report status or firlds:{update_fields} changed'
    notification = Notification(report=instance, user=instance.user, sent_at=timezone.now,
                                message=message, is_read=False)
    notification.save()
    print(notification)
    print(instance)
    print(created)
    print(update_fields)
