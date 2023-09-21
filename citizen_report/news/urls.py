from django.urls import path, include

from . import views

urlpatterns = [
    # path('news/<int:report_id>/', views.NewsPostList.as_view(), name='news'),
    path('reports/<int:report_id>/news/', views.news, name='news'),
    path('news/create-post/', views.NewsPostCreate.as_view(), name='create_post'),
    # path('news/<int:detail_id>/', views.detail, name='detail_post'),
    path('news/<int:pk>/', views.PostDetail.as_view(), name='detail_post'),
]