from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Report(models.Model):
    CATEGORY_CHOICES = [
        ('RBR', 'Roads and bridges'),
        ('SWS', 'Sewer and waterworks'),
        ('POW', 'Power supply'),
        ('GAS', 'Gasworks'),
        ('TEL', 'Telecommunication'),
        ('GAR', 'Garbage disposal'),
        ('CTR', 'City transport'),
        ('HTH', 'Healthcare'),
        ('EDU', 'Education'),
        ('SAF', 'Public safety')
    ]
    STATUS_CHOICES = [
        ('FR', 'Fresh report'),
        ('CH', 'Checking'),
        ('VD', 'Veryfied'),
        ('AP', 'Approved'),
        ('WP', 'Work in progres'),
        ('EW', 'Evaluation of works'),
        ('CD', 'Closed - done'),
    ]
    title = models.CharField(max_length=120)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='FR')
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    clerk = models.ForeignKey(User, related_name='assigned_reports', on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.title} | {self.created_at}'