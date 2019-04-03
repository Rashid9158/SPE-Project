from django import forms
from .models import Package
import re

class NewEntryForm(forms.ModelForm):
	class Meta:
		model = Package
		fields = ['phone','orderedfrom','productid']
