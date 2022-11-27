from django.contrib import admin

# Register your models here.
from .models import Address, Company, Person

admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Person)