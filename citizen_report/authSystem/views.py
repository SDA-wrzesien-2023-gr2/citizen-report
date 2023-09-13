from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class UserView(DetailView):
    template_name = 'profile.html'

    def get_object(self, **kwargs):
        return self.request.user


class PasswordChange(generic.FormView):
    model = get_user_model()
    form_class = PasswordChangeForm
    success_url = reverse_lazy("home")
    template_name = "change_password.html"

    def get_form_kwargs(self):
        kwargs = super(PasswordChange, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(PasswordChange, self).form_valid(form)

