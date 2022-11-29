from django.urls import path
from .views import *

app_name = 'clients'

urlpatterns = [
    path('',ClientListView.as_view(),name='clientsList'),
    path('add/',ClientCreateView.as_view(),name='add_client'),
    path('<int:pk>/',ClientDetailView.as_view(),name='client_detail'),
    path('<int:pk>/update',ClientUpdateView.as_view(),name='client_update'),
    path('<int:pk>/add',ClientContactAddView.as_view(),name='client_contact_create'),
    path('<int:pk>/update_contact',ClientContactUpdateView.as_view(),name='client_contact_update'),
    path('<int:pk>/delete',ClientContactDeleteView.as_view(),name='client_contact_delete'),
    path('load-client_contacts/', load_client_contact, name='ajax_load_client_contacts'),
]