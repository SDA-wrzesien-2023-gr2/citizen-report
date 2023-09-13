from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/authSystem/login'), name='logout'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("user/password_change/", views.PasswordChange.as_view(), name="password_change"),
    path('user/', login_required(views.UserView.as_view()), name='profile'),
    path('user/password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('user/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('user/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]