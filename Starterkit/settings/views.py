from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import AppSettings
from django.contrib.auth.models import User, Group
from notifications.models import Notification, add_group_notification, add_user_notification
from django.urls import reverse_lazy
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

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


class UserListView(ListView):
    model = User
    template_name = 'settings/user_list.html'
    fields = '__all__'

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('settings:users')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AddUser(View):
    def get(self,request,message="",errors=[]):
        context = {
            'errors': errors,
        }
        if len(message) > 0:
            context['message'] = message
        if request.user.username != 'admin':
            context['message'] = 'Please contact the admin user'
        return render(request,'settings/add_user.html',context)
    def post(self,request):
        p = request.POST
        print(p)
        username = p['username']
        email = p['email']
        firstname = p['firstname']
        lastname = p['lastname']
        password = p['password']
        repass = p['repassword']
        errors = []
        superuser = True if 'superuser' in p else False
        # return self.get(request)
        # Username
        if len(username) < 3:
            errors.append('Username should have at least 3 characters')
        if not re.match(r"^([a-z]+)+$", username):
            errors.append("Username should only contain lower case characters")
        if User.objects.filter(username=username).exists():
            errors.append('Username already in use')
        # Email
        try:
            validate_email(email)
        except ValidationError as e:
            errors.append('Invalid email ' + str(e))
        # First name
        if len(firstname) < 3:
            errors.append('First name should have at least 3 characters')
        # Last name
        if len(lastname) < 3:
            errors.append('Last name should have at least 3 characters')
        if len(password) < 8:
            errors.append('Password is too small')
        if password != repass:
            errors.append("Passwords don't match")
        if request.user.username != 'admin':
            return self.get(request)
        elif len(errors) > 0:
            return self.get(request,errors=errors)
        else:
            User.objects.create_user(
                username = username,
                email = email,
                first_name = firstname,
                last_name = lastname,
                is_staff = True,
                is_superuser = superuser,
            )
            return self.get(request,message="User has been created")

class AddGroup(View):
    def get(self,request,message="",errors=[]):
        context = {
            'errors': errors,
        }
        if len(message) > 0:
            context['message'] = message
        if request.user.username != 'admin':
            context['message'] = 'Please contact the admin user'
        return render(request,'settings/add_user.html',context)
    def post(self,request):
        p = request.POST
        username = p['username']
        email = p['email']
        firstname = p['firstname']
        lastname = p['lastname']
        password = p['password']
        repass = p['repassword']
        
        errors = []
        # Username
        if len(username) < 3:
            errors.append('Username should have at least 3 characters')
        if not re.match(r"^([a-z]+)+$", username):
            errors.append("Username should only contain lower case characters")
        if User.objects.filter(username=username).exists():
            errors.append('Username already in use')
        # Email
        try:
            validate_email(email)
        except ValidationError as e:
            errors.append('Invalid email ' + str(e))
        # First name
        if len(firstname) < 3:
            errors.append('First name should have at least 3 characters')
        # Last name
        if len(lastname) < 3:
            errors.append('Last name should have at least 3 characters')
        if len(password) < 8:
            errors.append('Password is too small')
        if password != repass:
            errors.append("Passwords don't match")
        if request.user.username != 'admin':
            return self.get(request)
        elif len(errors) > 0:
            return self.get(request,errors=errors)
        else:
            User.objects.create_user(
                username = username,
                email = email,
                first_name = firstname,
                last_name = lastname,
                is_staff = True,
            )
            return self.get(request,message="User has been created")