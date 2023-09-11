from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', views.show_reports, name='reports'),
    path('create/', views.create, name='create'),
    path('reports/<int:report_id>/', views.detail, name='detail')
]