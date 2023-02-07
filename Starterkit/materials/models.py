from django.db import models
from django.db.models import Q
from projects.models import file_size
from django.contrib.auth.models import User, Group
from projects.models import *
from clients.models import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from notifications.models import Notification, add_group_notification
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
    
    @property
    def get_inventory_url(self):
        return f"{reverse('materials:inventory_list')}?search={self.name}"
    
    
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
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
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
    def get_absolute_url(self):
        return reverse('materials:warehouse_update', kwargs={'pk': self.id})

    @property
    def update_url(self):
        return reverse('materials:warehouse_update', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:warehouse_delete', kwargs={'pk': self.id})


class Inventory(models.Model):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    owner = models.ForeignKey(Client,on_delete=models.DO_NOTHING, default=None)
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
            models.UniqueConstraint(fields=['material_id','warehouse_id','owner_id'],name = 'uniq_owner_inventory'),
        ]

    def __str__(self):
        return f'{self.material.name}-{self.warehouse.name}'
     
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Inventory,self).save(*args,**kwargs)
        if not is_new:
            title = text = ""
            if self.quantity == 0:
                title = "No inventory alert"
                text = f"Ran out of {self.material.name} at {self.warehouse.name} warehouse."
            elif self.quantity <= self.low_level:
                title = "Low inventory alert"
                text = f"Running out of {self.material.name} at {self.warehouse.name} warehouse. It has alread crossed the danger level of {self.low_level} and only {self.quantity} items are remaining."
            if title != "":
                for gname in ['admin']:
                    g = Group.objects.get(name=gname)
                    print(title,text,g)
                    add_group_notification(g,title,text)

    @property
    def update_url(self):
        return reverse('materials:inventory_update',kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('materials:inventory_delete',kwargs={'pk': self.id})

    @property
    def bgcolor(self):
        if self.quantity == 0:
            return "#ff0000"
        elif self.quantity <= self.low_level:
            return "#ffcc99"
        else:
            return "#adebad"


class InventoryAdjustment(models.Model):
    inventory = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    adjustment_amount = models.DecimalField(max_digits=10,decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    notes = models.CharField(max_length=30,default="")
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = FirstManager()  

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()  
    
    @property
    def get_absolute_url(self):
        return reverse('materials:purchase_detail',kwargs={'pk':self.pk})
    
    @property
    def get_update_url(self):
        return reverse('materials:purchase_update',kwargs={pk:self.pk})

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

    def save(self,*args,**kwargs):
        super(MaterialQty,self).save(*args,**kwargs)
        if self.purchase.warehouse:
            inventory = Inventory.objects.get_or_create(
                material = self.material,
                warehouse = self.purchase.warehouse
            )[0]
            inventory.quantity += float(self.quantity)
            inventory.save()
            InventoryAdjustment(
                inventory = inventory,
                adjustment_amount = self.quantity,
                user = self.purchase.user,
                notes = f"Purchased {self.quantity} on {self.purchase.date}"
            ).save()
        

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
    
    @property
    def get_list_url(self):
        return reverse('materials:transfer_list')
    
    

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



    
