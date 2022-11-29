from django.db import models
from projects.models import file_size
from django.contrib.auth.models import User
from projects.models import *
from clients.models import *
from django.urls import reverse
# Create your models here.


# models related to Material
class Category(models.Model):
    name = models.CharField(max_length=50)

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
    units = models.ForeignKey(Units,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='material/',validators=[file_size],blank=True)

    def __str__(self):
        return self.name
    
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



class InventoryAdjustment(models.Model):
    inventory = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    adjustment_amount = models.DecimalField(max_digits=10,decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return f'{self.inventory}#{self.adjustment_amount}'

    

# # models related to purchases


# class PurchaseStatus(models.Model):
#     name = models.CharField(max_length=10)
#     def __str__(self):
#             return self.name

# class MaterialQty(models.Model):
#     material = models.ForeignKey(Material,on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10,decimal_places=2)


# class Purchase(models.Model):
#     date = models.DateField()
#     description = models.TextField()
#     supplier = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
#     warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
#     materials = models.ManyToManyField(MaterialQty)
#     project = models.ForeignKey(Project,on_delete=models.DO_NOTHING,null=True)
#     status = models.ForeignKey(PurchaseStatus,on_delete=models.DO_NOTHING)
#     user = models.ForeignKey(User,on_delete=models.DO_NOTHING)

# # Models on transfers
# class MaterialTransfer(models.Model):
#     inventory = models.ForeignKey(Inventory,on_delete=models.DO_NOTHING)
#     quantity = models.ManyToManyField(MaterialQty)
#     project = models.ForeignKey(Project,on_delete=models.SET_NULL)
#     date = models.DateField()
#     user = models.ForeignKey(User,on_delete=models.DO_NOTHING)







    
