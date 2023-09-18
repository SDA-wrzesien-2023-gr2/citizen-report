from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from .constants import Category, Status

User = get_user_model()

class Report(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    clerk = models.ForeignKey(User, related_name='assigned_reports', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} | {self.created_at}'

    def save(self, *args, **kwargs):
        if not self.clerk:
            available_clerks = User.objects.filter(department=self.category).all()
            for clerk in available_clerks:
                clerk_count = clerk.assigned_reports.all().count()
                if clerk == available_clerks[0]:
                    prev_clerk_count = clerk_count
                    available_clerk = clerk
                else:
                    if prev_clerk_count > clerk_count:
                        available_clerk = clerk
                        prev_clerk_count = clerk_count
            self.clerk = available_clerk
        return super().save(*args, **kwargs)