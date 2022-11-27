from django.urls import path,include
from .views import *

app_nam = 'deals'
urlpatterns = [
    path('',DealsListView.as_view(), name='deals'),
    path('add/',DealsCreateView.as_view(),name='add_deal'),
    path('<int:pk>/',DealsDetailView.as_view(),name='deal_detail'),
]