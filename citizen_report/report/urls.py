from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', views.list_reports, name='reports'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('create/', views.create, name='create'),
    path('reports/<int:report_id>/', views.detail, name='detail'),
    path('update-report/<int:report_id>/', views.update_status, name='update_report'),
]
