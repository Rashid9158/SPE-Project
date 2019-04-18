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
        ], primary_key=True)
    orderedfrom = models.CharField(max_length=300, blank=False)
    productid = models.IntegerField(null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.phone


class DelPackage(models.Model):
    phone = models.CharField(max_length=10)
    orderedfrom = models.CharField(max_length=300)
    productid = models.IntegerField()
    quantity = models.IntegerField()
    datetime = models.CharField(max_length=50)

    def __str__(self):
        return self.phone+"("+str(self.productid)+")"