from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/authSystem/login'), name='logout'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("change_password/", views.PasswordChange.as_view(), name="change_password"),
    path('profile/', login_required(views.UserView.as_view()), name='profile'),
]