from django.db import models
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
        return f'{self.report}, {self.user}, {self.sent_at}, {self.message}, {self.is_read}'
