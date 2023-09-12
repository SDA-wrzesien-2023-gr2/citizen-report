from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    class Category(models.TextChoices):
        ROADS_AND_BRIDGES = 'RBR', _('Roads and bridges'),
        SEWER_AND_WATERWORKS = 'SWS', _('Sewer and waterworks'),
        POWER_SUPPLY = 'POW', _('Power supply'),
        GASWORKS = 'GAS', _('Gasworks'),
        TELECOMMUNICATION = 'TEL', _('Telecommunication'),
        GARBAGE_DISPOSAL = 'GAR', _('Garbage disposal'),
        CITY_TRANSPORT = 'CTR', _('City transport'),
        HEALTHCARE = 'HTH', _('Healthcare'),
        EDUCATION = 'EDU', _('Education'),
        PUBLIC_SAFETY = 'SAF', _('Public safety')

    class Status(models.TextChoices):
        PENDING = 'FR', _('Pending'),
        CHECKING = 'CH', _('Checking'),
        REJECTED = 'VD', _('Rejected'),
        APPROVED = 'AP', _('Approved'),

    title = models.CharField(max_length=120)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    status = models.CharField(max_length=2, choices=Status.choices, default='FRESH_REPORT')
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    clerk = models.ForeignKey(User, related_name='assigned_reports', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} | {self.created_at}'
