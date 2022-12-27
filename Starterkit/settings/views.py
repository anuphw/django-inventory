from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import AppSettings
from django.contrib.auth.models import User, Group
from notifications.models import Notification, add_group_notification, add_user_notification
from django.urls import reverse_lazy
from datetime import datetime



class SettingsPage(View):
    def get(self,request):
        settings,_ = AppSettings.objects.get_or_create()
        context = {
            'settings': settings,
        }
        return render(request,'settings/settings.html',context)
    def post(self,request):
        p = request.POST
        settings,_ = AppSettings.objects.get_or_create()
        settings.company_name = p['company_name']
        settings.phone_number = p['phone_number']
        settings.address = p['address']
        settings.email = p['email']
        text = 'something in settings changed'
        admin = Group.objects.get(name='admin')
        add_group_notification(admin,'Admin group notification', 'this is a group notification')

        if 'logo' in request.FILES:
            print(p)
            settings.logo = request.FILES['logo']
            print('we have logo')
            print(request.FILES)
        settings.save()
        return self.get(request)

class AppSettingsUpdateView(FormView):
    model = AppSettings
    template_name = 'settings/settings.html'
    fields = '__all__'
    success_url = reverse_lazy('settings:settings')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = AppSettings.objects.get_or_create()
        return context