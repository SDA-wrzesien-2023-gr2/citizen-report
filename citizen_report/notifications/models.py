from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

Report = 'report.Report'
User = 'authSystem.User'


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
def create_notification(sender, instance, **kwargs):
    notification = Notification(report=instance, user=instance.user, sent_at=timezone.now,
                                message='zmiana lub dodanie', is_read=False)
    print(notification)
    print(instance)

