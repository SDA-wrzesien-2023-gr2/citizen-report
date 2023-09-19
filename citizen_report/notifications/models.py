from django.db import models

Report = 'report.Report'
User = 'authSystem.User'


class Notification(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
