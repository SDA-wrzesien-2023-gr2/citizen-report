from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include

from . import views

urlpatterns = [
    path('reports/<int:pk>/news/', views.NewsPostList.as_view(), name='news'),
    path('reports/<int:pk>/create-news/', staff_member_required(views.NewsPostCreate.as_view()), name='create_news'),
    path('news/<int:pk>/', views.NewsPostDetail.as_view(), name='detail_news'),
    path('news/<int:pk>/comment/', views.NewsCommentCreate.as_view(), name='add_comment_to_news'),
]