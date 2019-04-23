from rest_framework import serializers

from .models import Package, DelPackage

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'



class DelPackageSerializer(serializers.ModelSerializer):
	class Meta:
		model = DelPackage
		fields = ('productid', 'phone', 'orderedfrom', 'quantity', 'datetime', 'status', 'deliveredto')