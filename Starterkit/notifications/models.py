from django.db import models
from django.contrib.auth.models import User
from clients.models import FirstManager
from django.utils import timezone
from django.urls import reverse

# Create your models here.




class Notification(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    def viewed(self):
        self.viewed_at = timezone.now()
        self.save()
    @property
    def get_view_url(self):
        return reverse('notifications:view',kwargs={'pk':self.pk})
    
    @property
    def bgcolor(self):
        if self.viewed_at:
            return "none"
        else:
            return "lightblue"


def add_group_notification(group,title,note):
    for user in group.user_set.all():
        Notification(
            text = note,
            title= title,
            user = user,
        ).save()


def add_user_notification(user,title,note):
    Notification(
        text = note,
        title= title,
        user = user,
    ).save()
