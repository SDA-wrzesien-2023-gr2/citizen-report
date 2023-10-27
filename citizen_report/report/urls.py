from django.urls import path
from . import views
from .views import ReportListView, MyReportListView, ReportCreate

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', ReportListView.as_view(), name='reports'),
    path('my-reports/', MyReportListView.as_view(), name='my_reports'),
    path('create/', ReportCreate.as_view(), name='create'),
    path('reports/<int:report_id>/', views.detail, name='detail'),
    path('update-report/<int:report_id>/', views.update_status, name='update_report'),
]
