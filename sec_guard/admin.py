from django.contrib import admin

from .models import Package, DelPackage

# Register your models here.
admin.site.register(Package)
admin.site.register(DelPackage)