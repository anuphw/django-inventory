from django.db import models

# Product
# Category (product category)
# Brand (product brand);
# Customer
# Supplier
# Order
# Job
# Material
# 


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
