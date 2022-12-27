from django.db import models
from django.db.models import Q
from projects.models import file_size
from django.contrib.auth.models import User
from projects.models import *
from clients.models import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.


# models related to Material
class Category(models.Model):
    name = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    @property
    def update_url(self):
        return reverse('materials:category_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:category_delete', kwargs={'pk': self.id})

class Brand(models.Model):
    name = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    @property
    def update_url(self):
        return reverse('materials:brand_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:brand_delete', kwargs={'pk': self.id})

class Units(models.Model):
    name = models.CharField(max_length=10)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    @property
    def update_url(self):
        return reverse('materials:unit_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:unit_delete', kwargs={'pk': self.id})

class Material(models.Model):
    name = models.CharField(max_length=20,null=False)
    code = models.CharField(max_length=6,null=False,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    unit = models.ForeignKey(Units,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='material/',validators=[file_size],blank=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    
    def get_level(self,warehouse_id):
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        inventory = Inventory.objects.filter(material=self,warehouse=warehouse).first()
        return inventory.quantity
    
    
    def get_low_level(self,warehouse_id):
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        inventory = Inventory.objects.filter(material=self,warehouse=warehouse).first()
        return inventory.low_level
    @property
    def update_url(self):
        return reverse('materials:material_update',kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:material_delete',kwargs={'pk': self.id})
    
    @property
    def img(self):
        return self.image.url



# Models related to warehouses
class City(models.Model):
    name = models.CharField(max_length=20)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    @property
    def update_url(self):
        return reverse('materials:city_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:city_delete', kwargs={'pk': self.id})


class Warehouse(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    @property
    def update_url(self):
        return reverse('materials:city_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:city_delete', kwargs={'pk': self.id})


class Inventory(models.Model):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    low_level = models.IntegerField(default=10)
    quantity = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['material_id','warehouse_id'],name = 'uniq_inventory'),
        ]

    def __str__(self):
        return f'{self.material.name}-{self.warehouse.name}'
     
    
    @property
    def update_url(self):
        return reverse('materials:inventory_update',kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:inventory_delete',kwargs={'pk': self.id})

    @property
    def bgcolor(self):
        if self.quantity <= self.low_level:
            return "#ffcc99"
        else:
            return "#adebad"


class InventoryAdjustment(models.Model):
    inventory = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    adjustment_amount = models.DecimalField(max_digits=10,decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
    

    def __str__(self):
        return f'{self.inventory}#{self.adjustment_amount}'

    

# models related to purchases



class Purchase(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=50)
    supplier = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING,null=True, blank=True)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING,null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()  

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  
    

class MaterialQty(models.Model):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()



# Models on transfers
class MaterialTransfer(models.Model):
    date = models.DateField()
    source = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING,related_name='source')
    destination = models.ForeignKey(Warehouse,on_delete=models.SET_NULL,null=True, blank=True,related_name='destination')
    project =  models.ForeignKey(Project,on_delete=models.SET_NULL,null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    @property
    def get_absolute_url(self):
        return reverse('materials:transfer_detail',kwargs={'pk':self.id})
    
    @property
    def delete_url(self):
        return reverse('materials:transfer_delete', kwargs={'pk': self.id})
    
    

class MaterialQtyTransfer(models.Model):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    transfer = models.ForeignKey(MaterialTransfer,on_delete=models.CASCADE)


class MaterialReturn(models.Model):
    date = models.DateField()
    project =  models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory,on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()



    
