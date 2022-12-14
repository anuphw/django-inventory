from django.db import models
from projects.models import Project
from materials.models import Warehouse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
# Create your models here.

class ExpenseCat(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    @property
    def update_url(self):
        return reverse('expenses:expcategory_update',kwargs={'pk':self.id})

    @property
    def delete_url(self):
        return reverse('expenses:expcategory_delete',kwargs={'pk':self.id})

class Expense(models.Model):
    date = models.DateField()
    details = models.TextField()
    category = models.ForeignKey(ExpenseCat,on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, null=True)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING,null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_absolute_url(self):
        return reverse('expenses:expense_detail',kwargs={'pk':self.id})
    
    @property
    def get_delete_url(self):
        return reverse('expenses:expense_delete',kwargs={'pk':self.id})
    
    @property
    def get_update_url(self):
        return "#"