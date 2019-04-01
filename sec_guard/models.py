from django.db import models

#create your models here
class Package(models.Model):
    phone = models.CharField(max_length=10, blank=False)
    orderedfrom = models.CharField(max_length=50, blank=False)
    productid= models.IntegerField()
    taken= models.BooleanField(default=False)
