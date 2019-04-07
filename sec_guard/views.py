from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from .forms import NewEntryForm
from twilio.rest import Client
from delservice import settings
from botocore.client import Config
import random
import json
import qrcode
import boto3
import cloudinary, cloudinary.uploader

# Create your views here.
def index(request):
	return render(request, 'sec_guard/index.html')

def new_entry(request):
	if request.method == 'POST':
		new_entry_form = NewEntryForm(request.POST)

		if new_entry_form.is_valid():

			new_entry_detail = {'phone': request.POST['phone'], 'orderedfrom': request.POST['orderedfrom'], 'productid': request.POST['productid']}
			new_entry_json = json.dumps(new_entry_detail)
			
			# qr code generation
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2,)
			qr.add_data(new_entry_json)
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save('image.jpg');

			# To store on cloudinary and getting url
			# res = cloudinary.uploader.upload('image.jpg', format='jpg', public_id= new_entry_detail['productid'])
			# img_url = res['url']

			# To store on s3 bucket AWS and getting url
			image_body = open('image.jpg', 'rb')
			config = Config(signature_version='s3v4')
			s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_ACCESS_SECRET_KEY, config=Config(signature_version='s3v4'))
			s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key =new_entry_detail['productid'] + '.jpg', Body =image_body)
			img_url = "https://s3.ap-south-1.amazonaws.com/{0}/{1}".format(settings.AWS_BUCKET_NAME, new_entry_detail['productid'] + '.jpg')

			# Twilio for messaging
			client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)			
			message = client.messages.create(to ='+91' + new_entry_detail['phone'], from_=settings.TWILIO_DEFAULT_CALLERID, body =img_url)

			new_entry_form.save()

			messages.success(request, 'QR code generated and has been sent successfully')
			return HttpResponseRedirect(reverse('sec_guard:index'))
		else:
			return render(request, 'sec_guard/new_entry.html', {'new_entry_form': new_entry_form})
	else:
		random.seed(datetime.now())		
		new_entry_form = NewEntryForm(initial={'productid': random.randint(100000,999999)}) 
		return render(request, 'sec_guard/new_entry.html', {'new_entry_form': new_entry_form})

def search_by_phone(request):
	return render(request, 'sec_guard/search_by_phone.html')

def detail(request):
	random.seed(datetime.now())
	detail={'phone': request.POST['phone'], 'orderedfrom': request.POST['orderedfrom']}
	return render(request, 'sec_guard/detail.html', detail)