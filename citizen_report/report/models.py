from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ReportModel(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField()
    status = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caretaker = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.title} | {self.date}'