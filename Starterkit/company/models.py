from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=250)
    contact = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.address

class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=15)
    designation = models.CharField(max_length=15)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
