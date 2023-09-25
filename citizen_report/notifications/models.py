from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from report.models import Report

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.report, self.user, self.sent_at, self.message, self.is_read


# UNDER CONSTRUCTION:
@receiver(post_save, sender=Report)
def create_notification(sender, created, instance, update_fields, **kwargs):
    message = f'new report {instance.title} added!' if created else f'report status or fields:{update_fields} changed'
    notification = Notification(report=instance, user=instance.user, sent_at=timezone.now,
                                message=message, is_read=False)
    notification.save()
    clerk = instance.clerk
    send_mail(
        f'subject: {message}',
        f'{repr(notification)}',
        f'{clerk.email}',
        [f'{instance.user.email}'],
    )
    print(notification)
    print(instance)
    print(created)
    print(update_fields)
