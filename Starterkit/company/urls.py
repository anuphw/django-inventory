from django.urls import path,include
from .views import *

urlpatterns = [
    path('newCompany',newCompanyView.as_view(),name='newCompany')
]