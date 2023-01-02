from .models import *
from datetime import timedelta
from django.utils import timezone

def notifications(request):
    since = timezone.now().date() - timedelta(days=3)
    context = {}
    if request.user.id:
        context = {
            'notifications': request.user.notification_set.filter(created_at__gte = since).order_by('-created_at').all(),
            'unread_count': request.user.notification_set.filter(created_at__gte = since).filter(viewed_at__isnull = True).count()
        }
    return context