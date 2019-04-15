from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

#create your models here
class Package(models.Model):
    phone = models.CharField(max_length=10, 
    	validators=[
            RegexValidator(
                r'^[0-9]*$',
                'Only 0-9 are allowed.',
                'Invalid Number'
            ),
            MinLengthValidator(10),
            MaxLengthValidator(10),
        ],)
    orderedfrom = models.CharField(max_length=20, blank=False)
    productid= models.IntegerField(primary_key=True)
    taken= models.BooleanField(default=False)

    def __str__(self):
        return str(self.productid)
