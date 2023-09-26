from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'text', 'image', 'category')


class UpdateReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('status',)
