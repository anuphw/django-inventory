"""skote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from skote import views
from .views import MyPasswordSetView ,MyPasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboards View
    path('',views.DashboardView.as_view(),name='dashboard'),    
   
    # Layouts
    path('layout/',include('layout.urls')),

    # Inventory
    path('inventory/',include('inventory.urls')),
    path('clients/',include('clients.urls', namespace='clients')),
    path('projects/',include('projects.urls', namespace='projects')),
    path('materials/',include('materials.urls', namespace='materials')),
    #Authencation
    # path('authentication/',include('authentication.urls')),
    #Pages
    path('pages/',include('pages.urls')),
    # Allauth
    path('account/', include('allauth.urls')),
    path('auth-logout/',TemplateView.as_view(template_name="account/logout-success.html"),name ='pages-logout'),
    path('auth-lockscreen/',TemplateView.as_view(template_name="account/lock-screen.html"),name ='pages-lockscreen'),
        #Custum change password done page redirect
    path('accounts/password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    #Custum set password done page redirect
    path('accounts/password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
