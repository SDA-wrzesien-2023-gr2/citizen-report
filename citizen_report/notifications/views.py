from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Notification


# Create your views here.

# UNDER CONSTRUCTION!!!

class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification_detail.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        Notification.objects.filter(pk=self.kwargs['pk']).update(is_read=True)
        return queryset.filter(id=self.kwargs['pk'])


class NotificationListView(ListView):
    model = Notification
    paginate_by = 5
    template_name = 'my_notifications.html'

