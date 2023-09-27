from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from models import Notification


# Create your views here.

# UNDER CONSTRUCTION!!!
class NotificationCreateView(CreateView):
    model = 'Notification'
    template_name = 'TEMPLATE_NAME'


class NotificationDetailView(DetailView):
    model = 'Notification'
    template_name = 'TEMPLATE_NAME'


class NotificationListView(ListView):
    model = 'Notification'
    template_name = 'TEMPLATE_NAME'


class NotificationsUpdateView(UpdateView):
    model = 'Notifications'
    template_name = 'TEMPLATE_NAME'
