from django.urls import path,include
from .views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settings'

urlpatterns = [
    path('',SettingsPage.as_view(),name='settings'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)