from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail

from report.models import Report
from news.models import NewsPost, NewsComment
from notifications.models import Notification


@receiver(post_save, sender=Report)
def create_report_notification(sender, created, instance, update_fields, **kwargs):
    message = f'New report "{instance.title}" has been added!' if created else f'Report "{instance.title}": status has been changed'
    notification = Notification(report=instance, user=instance.user,
                                message=message, is_read=False)
    notification.save()


@receiver(post_save, sender=NewsPost)
def create_news_notification(sender, created, instance, update_fields, **kwargs):
    message = f'New post "{instance.title}" has been added to "{instance.report.title}"!'
    notification = Notification(report=instance.report, user=instance.report.user,
                                message=message, is_read=False)
    notification.save()


@receiver(post_save, sender=NewsComment)
def create_comment_notification(sender, created, instance, update_fields, **kwargs):
    message = f'New comment has been added to "{instance.post.title}"!'
    notification = Notification(report=instance.post.report, user=instance.user,
                                message=message, is_read=False)
    notification.save()


@receiver(post_save, sender=Notification)
def send_email(sender, created, instance, update_fields, **kwargs):
    send_mail(
        f'subject: {instance.message}',
        f'{repr(instance)}',
        f'helpdesk@reports.cem',
        [f'{instance.user.email}'],
    )
