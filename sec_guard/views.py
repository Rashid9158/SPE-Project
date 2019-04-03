from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from .forms import NewEntryForm
import random

# Create your views here.
def index(request):
	return render(request, 'sec_guard/index.html')

def new_entry(request):
	if request.method == 'POST':
		new_entry_form = NewEntryForm(request.POST)

		if new_entry_form.is_valid():
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
	detail={'phone': request.POST['phone'], 'orderedfrom': request.POST['orderedfrom'], 'productid': random.randint(10000,99999)}
	return render(request, 'sec_guard/detail.html', detail)