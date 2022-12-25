from django.db import models
from projects.models import file_size
from django.contrib.auth.models import User
from django.core.validators import validate_email
# Create your models here.


class AppSettings(models.Model):
    company_name = models.CharField(max_length=50,default='Company Name')
    email = models.CharField(max_length=30,default='abc@example.com',validators=[validate_email])
    phone_number = models.CharField(max_length=20,default='+91 999 999 9999')
    website = models.CharField(max_length=50,default='www.example.com')
    address = models.CharField(max_length=50,default='default address')
    logo = models.ImageField(upload_to='settings/',validators=[file_size],blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    
