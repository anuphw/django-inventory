from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class FirstManager(models.Manager):

    def get_queryset(self):
        try:
            return super().get_queryset().filter(deleted_at__isnull = True)
        except:
            return super().get_queryset()

    def get_first(self,pk):
        try:
            return super().get_queryset().filter(pk=pk).first()
        except:
            return None




class Client(models.Model):
    name = models.CharField(null=False, max_length=50, unique=True)
    address = models.CharField(null=False, max_length=200)
    contact_number = models.CharField(null=False, max_length=15)
    is_active = models.BooleanField(default=True)
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  

    def __str__(self):
        return self.name
        
    @property
    def get_absolute_url(self):
        return reverse('clients:client_detail', kwargs={'pk':self.pk})
    
class ClientContact(models.Model):
    name = models.CharField(null=False, max_length=15)
    contact_number = models.CharField(null=False, max_length=15)
    designation = models.CharField(max_length=10,null=False,default='Manager')
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  
        
    def get_absolute_url(self):
        return reverse('clients:client_contact_update', kwargs={'pk':self.pk})      
    
    def get_delete_url(self):
        return reverse('clients:client_contact_delete', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}-{self.client.name}"
