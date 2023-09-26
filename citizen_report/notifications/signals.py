from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail

from report.models import Report
from news.models import NewsPost, NewsComment
from notifications.models import Notification


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

@receiver(post_save, sender=NewsPost)
def create_notification(sender, created, instance, update_fields, **kwargs):
    message = f'new evaluation {instance.title} added!'
    notification = Notification(report=instance.report, user=instance.report.user, sent_at=timezone.now,
                                message=message, is_read=False)
    notification.save()
    print(notification)
@receiver(post_save, sender=NewsComment)
def create_notification(sender, created, instance, update_fields, **kwargs):
    message = f'new comment to {instance.post} added!'
    notification = Notification(report=instance.post.report, user=instance.user, sent_at=timezone.now,
                                message=message, is_read=False)
    notification.save()
    print(notification)
