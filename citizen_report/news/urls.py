from django.urls import path, include

from . import views

urlpatterns = [
    path('reports/<int:pk>/news/', views.NewsPostList.as_view(), name='news'),
    path('news/create-news/', views.NewsPostCreate.as_view(), name='create_news'),
    path('news/<int:pk>/', views.NewsPostDetail.as_view(), name='detail_news'),
    path('news/<int:pk>/comment/', views.NewsCommentCreate.as_view(), name='add_comment_to_news'),
]