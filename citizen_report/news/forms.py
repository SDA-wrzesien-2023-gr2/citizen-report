from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import NewsPost
# from report.models import Report


class NewsPostCreationForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ('report', 'title', 'text', 'image')


