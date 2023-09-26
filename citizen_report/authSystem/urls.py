from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/authSystem/login'), name='logout'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("user/change_password/", views.PasswordChange.as_view(), name="change_password"),
    path('user/', login_required(views.UserView.as_view()), name='profile'),
    path('user/reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('user/reset-password-confirm/<uidb64>/<token>/', views.ResetConfirmPasswordView.as_view(), name='reset_password_confirm'),
    path('user/reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/reset_password_complete.html'),
         name='reset_password_complete'),
    path("", include("django.contrib.auth.urls")),
]