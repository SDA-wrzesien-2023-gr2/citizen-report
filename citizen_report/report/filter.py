import django_filters

from .models import Report


class ReportFilter(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = ['category', 'status']


class MyReportFilter(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = ['status',]