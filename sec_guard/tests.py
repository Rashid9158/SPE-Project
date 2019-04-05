from django.test import TestCase

from .models import Package
# Create your tests here.

#Test Case for model
class PackageTest(TestCase):
	def create_package(self, phone="9876543210", orderedfrom="Amazon"):
		return Package.objects.create(orderedfrom=orderedfrom, productid=productid)

	def test_creation(self):
		w=self.create_package()
		self.assertTrue(isinstance(w,Package))