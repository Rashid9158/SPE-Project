from django.test import TestCase
from .models import Package, DelPackage
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . serializers import PackageSerializer, DelPackageSerializer
from datetime import datetime


# Test Case for model Package
class PackageModelTest(TestCase):
	def create_package(self, phone="9158399067", orderedfrom="myntra"):
		return Package.objects.create(phone=phone, orderedfrom=orderedfrom)

	def test_creation(self):
		w=self.create_package()
		self.assertTrue(isinstance(w,Package))


# Test case for APIs POST, GET and DELETE of model Package
class PackagePostGetDeleteTest(APITestCase):
	def test_create_package(self):
		url = reverse('package_create')
		data = {'phone':'9158399067', 'orderedfrom':'myntra'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(Package.objects.count(), 1)
		self.assertEqual(Package.objects.get().phone, '9158399067')

	def test_get_package(self, pk="9158399067"):
		Package.objects.create(phone="9158399067", orderedfrom="myntra")
		url = reverse('package_detail_deliver', args=["9158399067"])
		package = Package.objects.get(pk=pk)
		serializer = PackageSerializer(package)
		self.assertEqual(package.phone, serializer.data['phone'])
		self.assertEqual(package.orderedfrom, serializer.data['orderedfrom'])

	def test_delete_package(self):
		Package.objects.create(phone="9158399067", orderedfrom="myntra", productid="231004")
		url = reverse('package_detail_deliver', args=["9158399067"])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)





# Test Case for Model DelPackage 
class DelPackageModelTest(TestCase):
	def create_package(self, phone="9158399067", orderedfrom="myntra", datetime=str(datetime.now()), productid="231456", quantity=1):
		return DelPackage.objects.create(phone=phone, orderedfrom=orderedfrom, datetime=datetime, productid=productid, quantity=quantity)

	def test_creation(self):
		w=self.create_package()
		self.assertTrue(isinstance(w,DelPackage))


# Test Case for API GET for model DelPackage
class DelPackageGetTest(APITestCase):
	def test_get_package(self, phone="9158399067"):
		DelPackage.objects.create(phone="9158399067", orderedfrom="myntra", productid="431267", quantity=1)
		url = reverse('del_package_detail', args=["9158399067"])
		package = DelPackage.objects.get(phone=phone)
		serializer = PackageSerializer(package)
		self.assertEqual(package.phone, serializer.data['phone'])
		self.assertEqual(package.orderedfrom, serializer.data['orderedfrom'])