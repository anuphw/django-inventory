from django.urls import path,include
from .views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settings'

urlpatterns = [
    path('',SettingsPage.as_view(),name='settings'),
    path('addUser',AddUser.as_view(),name='add_user'),
    path('users',UserListView.as_view(),name='users'),
    path('<int:pk>/delete',UserDeleteView.as_view(),name='user_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)