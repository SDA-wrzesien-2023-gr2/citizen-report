from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Notification


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification_detail.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        Notification.objects.filter(pk=self.kwargs['pk']).update(is_read=True)
        return queryset.filter(id=self.kwargs['pk'])


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    paginate_by = 5
    template_name = 'my_notifications.html'

