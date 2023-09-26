from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


def assign_clerk(instance):
    available_clerks = User.objects.filter(department=instance.category).filter(is_staff=True).all()
    instance.clerk = available_clerks.annotate(num_reports=Count("assigned_reports")).order_by("num_reports").first()
    return instance.clerk