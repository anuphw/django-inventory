from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>',NotificationViewedView.as_view(),name='view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
