from django.db import models
import os
from django.db.models import Max
# Create your models here.

import datetime
from django.contrib.auth.models import User
from clients.models import Client, ClientContact, FirstManager
from skote.get_username import get_username
from django.urls import reverse

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
    status_rank = models.IntegerField(default=0)
    description = models.TextField()
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 


    def change_status(self,status,user):
        old_status = self.status
        self.status = status
        self.save()
        
    def change_status_rank(self,new_rank=None):
        old_rank = self.status_rank
        if new_rank is None:
            new_rank = Project.objects.filter(status=self.status).aggregate(Max('status_rank'))['status_rank__max'] + 1
            self.status_rank = new_rank
            self.save()
        else:
            for project in Project.objects.filter(status_rank__gte = new_rank).all():
                if project.id != self.id:
                    project.status_rank = project.status_rank + 1
                    project.save()
            self.status_rank = new_rank
            self.save()

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
    
    @property
    def create_challan_url(self):
        return reverse('projects:delivery_challan_create',kwargs={'pk':self.pk})

    @property
    def create_inward_challan_url(self):
        return reverse('projects:inward_material_create',kwargs={'pk':self.pk})
    
    @property
    def all_materials(self):
        materials = {} # material, quantity
        for purchase in self.purchase_set.all():
            for m in purchase.materialqty_set.all():
                materials[m.material.name] = [m,m.quantity]
        
        for transfer in self.materialtransfer_set.all():
            for m in transfer.materialqtytransfer_set.all():
                if m.material.name not in materials:
                    materials[m.material.name] = [m.material,0]
                materials[m.material.name][1] += m.quantity
        
        for rt in self.materialreturn_set.all():
            if rt.inventory.material.name not in materials:
                materials[rt.inventory.material.name] = [rt.inventory.material,0]
            materials[rt.inventory.material.name][1] -= rt.quantity
        return materials
    
    @property
    def all_products(self):
        products = {} # product, quantity, delivered, returned, remaining 
        for product in self.product_set.all():
            products[f'{product.id}'] = [product,product.quantity,0,0,product.quantity] # product, quantity, delivered, returned, remaining 
        for dc in self.deliverychallan_set.all():
            for dp in dc.deliveryproduct_set.all():
                if f'{dp.product.id}' in products.keys():
                    products[f'{dp.product.id}'][2] += dp.quantity
                    products[f'{dp.product.id}'][4] -= dp.quantity
        for ret in self.returns_set.all():
            for pr in ret.productreturn_set.all():
                if f'{pr.product.id}' in products.keys():
                    products[f'{pr.product.id}'][3] += pr.quantity
                    products[f'{pr.product.id}'][4] += pr.quantity
        return products

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
    vehicleNo = models.TextField(max_length=20,default="")
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

    @property
    def get_absolute_url(self):
        return reverse('projects:delivery_challan_update',kwargs={'pk':self.project.pk,'dc_id':self.pk})
    
    @property
    def get_pdf_url(self):
        return reverse('projects:delivery_challan_pdf',kwargs={'pk':self.project.pk,'dc_id':self.pk})
    
    @property
    def get_delete_url(self):
        return reverse('projects:delivery_challan_delete',kwargs={'pk':self.project.pk,'dc_id':self.pk})

    @property
    def get_return_url(self):
        return reverse('projects:delivery_return_create',kwargs={'pk':self.project.pk,'dc_id':self.pk})



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

class Returns(models.Model):
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    date = models.DateField()
    challan = models.ForeignKey(DeliveryChallan,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

class ProductReturn(models.Model):
    return_id = models.ForeignKey(Returns,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    notes = models.TextField()
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
    type = models.TextField(max_length=50,null=True)
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

# Inward material
class IMChallan(models.Model):
    challanNo = models.CharField(max_length=30)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = ProjectTimelineManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    @property
    def get_absolute_url(self):
        return reverse('projects:inward_material_update',kwargs={'pk':self.project.pk,'imc': self.pk})
    @property
    def get_update_url(self):
        return reverse('projects:inward_material_update',kwargs={'pk':self.project.pk,'imc': self.pk})
    @property
    def get_delete_url(self):
        return reverse('projects:inward_material_delete',kwargs={'pk':self.project.pk,'imc': self.pk})



class IMQty(models.Model):
    imchallan = models.ForeignKey(IMChallan,on_delete=models.DO_NOTHING)
    imaterial = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = ProjectTimelineManager() 

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


