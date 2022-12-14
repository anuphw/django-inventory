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
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Status(models.Model):
    status = models.CharField(max_length=20)
    order = models.PositiveSmallIntegerField(default=1)
    probability = models.IntegerField(default=50,validators=PERCENTAGE_VALIDATOR)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  
        
    class Meta:
        verbose_name_plural = '1. Statuses'

    def __str__(self) -> str:
        return f"{self.order} - {self.status}"

    @property
    def delete_url(self):
        return reverse('projects:status_delete',kwargs={'pk': self.id})





class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    contact_person = models.ManyToManyField(ClientContact)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  
    
    class Meta:
        verbose_name_plural = '2. Deals'

    
    def __str__(self) -> str:
        return self.title

    @property
    def company_contacts(self):
        return ClientContact.objects.filter(client=self.client)
    
    @property
    def selected_contacts(self):
        return self.contact_person.all()

    @property
    def get_delete_url(self):
        return reverse('projects:project_delete', kwargs={'pk':self.pk})

    @property
    def get_edit_url(self):
        return reverse('projects:project_update', kwargs={'pk':self.pk})

    @property
    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk':self.pk})
    
    @property
    def get_raw_return_url(self):
        return reverse('projects:project_return', kwargs={'pk':self.pk})
    

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  

    def __str__(self):
        return self.name

class DeliveryChallan(models.Model):
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    date = models.DateField()
    challanNo = models.CharField(max_length=10)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

class DeliveryProduct(models.Model):
    deliveryChallan = models.ForeignKey(DeliveryChallan,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class ProjectFiles(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/',validators=[file_size])
    notes = models.CharField(max_length=50,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  

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
    def get_queryset(self):
        try:
            return super().get_queryset().filter(deleted_at__isnull = True).order_by('-created_at')
        except:
            return super().get_queryset()




class ProjectTimeline(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    project_file = models.ForeignKey(ProjectFiles,on_delete=models.SET_NULL,null=True)
    notes = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = ProjectTimelineManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  

    class Meta:
        verbose_name_plural = '3. Project Timeline'
    
    def __str__(self):
        return self.notes



