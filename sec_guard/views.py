from django.shortcuts import render
from datetime import datetime
import random

# Create your views here.
def index(request):
	return render(request, 'sec_guard/index.html')

def new_entry(request):
	return render(request, 'sec_guard/new_entry.html')

def search_by_phone(request):
	return render(request, 'sec_guard/search_by_phone.html')

def detail(request):
	random.seed(datetime.now())
	detail={'phone': request.POST['phone'], 'orderedfrom': request.POST['orderedfrom'], 'productid': random.randint(10000,99999)}
	return render(request, 'sec_guard/detail.html', detail)