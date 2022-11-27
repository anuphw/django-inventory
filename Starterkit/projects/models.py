from django.db import models
import os
# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User
from clients.models import Client, ClientContact, FirstManager
from skote.get_username import get_username
from django.urls import reverse
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


STATUSES = (
    ('1','Inquiry'),
    ('2','Quotation Sent'),
    ('3','Negotation'),
    ('4','Processing'),
    ('5','Delivering'),
    ('6','Delivered'),
    ('7','Complete'),
    ('8','Cancelled'),
)



class Status(models.Model):
    status = models.CharField(max_length=20,choices=STATUSES)
    objects = FirstManager()
    class Meta:
        verbose_name_plural = '1. Statuses'

    def __str__(self) -> str:
        return self.get_status_display()



class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    contact_person = models.ManyToManyField(ClientContact)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    delivary_address = models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FirstManager()
    class Meta:
        verbose_name_plural = '2. Deals'

    
    def __str__(self) -> str:
        return self.title

    def get_delete_url(self):
        return reverse('projects:project_delete', kwargs={'pk':self.pk})

    def get_edit_url(self):
        return reverse('projects:project_update', kwargs={'pk':self.pk})

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk':self.pk})
    
class ProjectFiles(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/',validators=[file_size])
    notes = models.CharField(max_length=50,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file

    def get_file_url(self):
        try: 
            return self.file.url
        except:
            return ''
    
    def delete(self):
        self.file.delete()
        return super().delete()

    def get_file_name(self):
        try:
            return os.path.basename(self.file.url)
        except:
            return "File does not exist"
    
    def get_delete_url(self):
        return reverse('projects:file_delete', kwargs={'pk':self.pk})

class ProjectTimelineManager(models.Manager):
    def get_queryset(self) :
        return super().get_queryset().order_by('-created_at')

class ProjectTimeline(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    project_file = models.ForeignKey(ProjectFiles,on_delete=models.SET_NULL,null=True)
    notes = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectTimelineManager()
    class Meta:
        verbose_name_plural = '3. Project Timeline'
    
    def __str__(self):
        return self.notes
