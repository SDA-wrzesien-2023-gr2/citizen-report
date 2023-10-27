from .models import Notification


def unread_messages(request):
    return {
        'notifications': Notification.objects.filter(is_read=False)
    }
