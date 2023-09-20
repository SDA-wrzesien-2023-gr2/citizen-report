from django.urls import path, include

from . import views
from . import views

urlpatterns = [
    # path('news/<int:report_id>/', views.NewsPostList.as_view(), name='news'),
    path('news/<int:report_id>/', views.news, name='news'),
]