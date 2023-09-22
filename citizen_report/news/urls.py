from django.urls import path, include

from . import views

urlpatterns = [
    path('reports/<int:pk>/news/', views.NewsPostList.as_view(), name='news'),
    path('news/create-post/', views.NewsPostCreate.as_view(), name='create_post'),
    path('news/<int:pk>/', views.PostDetail.as_view(), name='detail_post'),
    path('news/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]