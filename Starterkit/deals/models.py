from django.db import models
import datetime
from django.contrib.auth.models import User
from clients.models import Client, ClientContact
from skote.get_username import get_username


STATUSES = (
    ('1','Inquiry'),
    ('2','Quotation Sent'),
    ('3','Negotation'),
    ('4','Processing'),
    ('5','Delivering'),
    ('6','Delivered'),
    ('7','Complete'),
)

class Status(models.Model):
    status = models.CharField(max_length=20,choices=STATUSES)

    class Meta:
        verbose_name_plural = '1. Statuses'

    def __str__(self) -> str:
        return self.status



class Deal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    contact_person = models.ForeignKey(ClientContact, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    delivary_address = models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    class Meta:
        verbose_name_plural = '2. Deals'

    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        status = Status.objects.filter(status = self.status).first()

        dt = DealTimeline(deal=self,status=status,notes = "",user = get_username())
        dt.save()
        

class DealTimeline(models.Model):
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    notes = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '3. Deal Timeline'
    
    def __str__(self):
        return self.notes
