from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Package, DelPackage
from .serializers import PackageSerializer, DelPackageSerializer
from django.http import Http404
from rest_framework import status
from twilio.rest import Client
from delservice import settings
from datetime import datetime
import qrcode, cloudinary, cloudinary.uploader
import random

class PackageCreate(APIView):

	def post(self, request, format=None):
		serializer = PackageSerializer(data=request.data)
		temp_package = Package.objects.filter(pk=serializer.initial_data['phone']).first()

		if temp_package==None:			
			if serializer.is_valid():
				# saving in database
				serializer.save()

				# random generator seeding and updating productid in DB
				random.seed(datetime.now())
				prod_id = random.randint(100000,999999)
				Package.objects.filter(pk=serializer.data['phone']).update(productid = prod_id)

				# qr code generation
				qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2,)
				qr.add_data({'productid':prod_id, 'phone':serializer.data['phone'], 'orderedfrom':serializer.data['orderedfrom']})
				qr.make(fit=True)
				img = qr.make_image(fill_color="black", back_color="white")
				img.save('image.jpg');

				# # To store on cloudinary and getting url
				# res = cloudinary.uploader.upload('image.jpg', format='jpg', public_id= prod_id)
				# img_url = res['url']

				# # Twilio for messaging
				# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
				# message = client.messages.create(to ='+91' + serializer.data['phone'], from_=settings.TWILIO_DEFAULT_CALLERID, body ="Get this qr code scanned " + img_url + " and collect your delivery from the reception. ")

			 	# returning response
				return Response({"message":prod_id})
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		else:
			Package.objects.filter(pk=temp_package.phone).update(orderedfrom = temp_package.orderedfrom + ", " + request.data['orderedfrom'], quantity=temp_package.quantity+1)
			temp_package.refresh_from_db()

			# qr code generation
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2,)
			qr.add_data({'productid':temp_package.productid, 'phone':temp_package.phone, 'orderedfrom':temp_package.orderedfrom})
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save('image.jpg');

			# # To store on cloudinary and getting url
			# res = cloudinary.uploader.upload('image.jpg', format='jpg', public_id= temp_package.productid)
			# img_url = res['url']

			# # Twilio for messaging
			# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
			# message = client.messages.create(to ='+91' + temp_package.phone, from_=settings.TWILIO_DEFAULT_CALLERID, body ="Get this qr code scanned " + img_url + " and collect your delivery from the reception. ")

			# returning response
			return Response({"message":temp_package.productid})



class PackageDetailDeliver(APIView):

	def get_object(self, pk):
		try:
			return Package.objects.get(pk=pk)
		except Package.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		package = self.get_object(pk)
		serializer = PackageSerializer(package)
		return Response(serializer.data)

	def delete(self, request, pk, format=None):
		package = self.get_object(pk)
		now = datetime.now()
		temp_package = DelPackage.objects.create(phone=package.phone, orderedfrom=package.orderedfrom, productid=package.productid, quantity=package.quantity, datetime=now.strftime("Date: %d %B %Y, Time: %I:%M %p"))
		package.delete()

		# # Twilio for messaging
		# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
		# message = client.messages.create(to ='+91' + temp_package.phone, from_=settings.TWILIO_DEFAULT_CALLERID, body ="Package Delivered. If its not you visit the reception")

		# sending response
		return Response({"message":"Package Delivered"})



class DelPackageDetail(APIView):

	def get_object(self, phone):
		try:
			return DelPackage.objects.filter(phone=phone)
		except DelPackage.DoesNotExist:
			raise Http404

	def get(self, request, phone, format=None):
		delpackage = self.get_object(phone)
		serializer = DelPackageSerializer(delpackage, many=True)
		return Response(serializer.data)














