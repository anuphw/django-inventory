from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .models import *

def viewed(request):
    pk = request.GET['pk']
    Notification.objects.get(pk=pk).viewed()

def view_all(request):
    for n in Notification.objects.filter(user = request.user):
        n.viewed()

class NotificationViewedView(View):
    def get(self,request,pk):
        Notification.objects.get(pk=pk).viewed()
        return HttpResponse('success')

class NotificationDetailView(View):
    def get(self,request,pk,message=""):
        notification = Notification.objects.get(pk=pk)
        if notification.user.id != request.user.id:
            message = 'Notification cannot be accessed!'
            return render(request,'notifications/notification_detail.html',{'message':message})
        else:
            # notification.viewed()
            return render(request,'notifications/notification_detail.html',{'notification':notification})

class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notifications_list.html'
    

    def get_queryset(self):
        nots = Notification.objects.filter(user = self.request.user).order_by('-created_at')[:50]
        return nots

