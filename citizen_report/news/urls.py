from django.urls import path, include

from . import views

urlpatterns = [
    path('news/', views.news, name='news'),
]