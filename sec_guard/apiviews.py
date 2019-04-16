from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Package
from .serializers import PackageSerializer
from django.http import Http404
from rest_framework import status
from twilio.rest import Client
from delservice import settings
import qrcode, cloudinary, cloudinary.uploader

class PackageCreate(APIView):

	def post(self, request, format=None):
		serializer = PackageSerializer(data=request.data)
		if serializer.is_valid():
			# saving in database
			serializer.save()

			# qr code generation
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2,)
			qr.add_data({'productid':serializer.data['productid'], 'phone':serializer.data['phone'], 'orderedfrom':serializer.data['orderedfrom']})
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save('image.jpg');

			# To store on cloudinary and getting url
			res = cloudinary.uploader.upload('image.jpg', format='jpg', public_id= serializer.data['productid'])
			img_url = res['url']

			# Twilio for messaging
			# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
			# message = client.messages.create(to ='+91' + serializer.data['phone'], from_=settings.TWILIO_DEFAULT_CALLERID, body ="Get this qr code scanned " + img_url + " and collect your delivery from the reception. ")

			# returning response
			return Response({"message":"QR code generated and has been sent successfully"}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PackageDetailId(APIView):

	def get_object(self, pk):
		try:
			return Package.objects.get(pk=pk)
		except Package.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		package = self.get_object(pk)
		serializer = PackageSerializer(package)
		return Response(serializer.data)
	


class PackageListPhone(APIView):

	def get_object(self, phone):
		try:
			return Package.objects.filter(phone=phone)
		except Package.DoesNotExist:
			raise Http404

	def get(self, request, phone, format=None):
		package = self.get_object(phone)
		serializer = PackageSerializer(package, many=True)
		return Response(serializer.data)




class PackageUpdate(APIView):

	def get_object(self, pk):
		try:
			return Package.objects.get(pk=pk)
		except Package.DoesNotExist:
			raise Http404

	def put(self, request, pk, format=None):
		package = self.get_object(pk)
		serializer = PackageSerializer(package, data=request.data)
		if serializer.is_valid():
			# saving in database
			serializer.save()

			# Twilio for messaging
			# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
			# message = client.messages.create(to ='+91' + serializer.data['phone'], from_=settings.TWILIO_DEFAULT_CALLERID, body ="Package Delivered. If its not you visit the reception")
			
			# returning response
			return Response({"message":"Package Delivered"})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)