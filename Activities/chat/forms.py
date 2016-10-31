import re
from django import forms
from authentication.models import User
from django.core.exceptions import ValidationError

def validatePhone(phone):
	if not re.match(r'^[0-9]{11}$', phone):
		raise ValidationError('Incorrect Phone')

def validateTelegram(telegram):
	if not re.match(r'^\@{1}[a-z,A-Z,0-9,_]*$', telegram):
		raise ValidationError('Incorrect Telegram')

def validateDate(date):
	if not re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', date):
		raise ValidationError('Incorrect Date')

def validateGender(gender):
	if not (gender == 'F' or gender =='M'):
		raise ValidationError('Incorrect Gender')

class ChatForm(forms.Form):
#	title = 'Chat of activity:'
    comment = forms.te
	phone = forms.CharField(label='Phone', max_length=11, widget=forms.Textarea, validators=[validatePhone])
	telegram = forms.CharField(label='Telegram',max_length=30,widget=forms.Textarea,validators=[validateTelegram])
	birth_date = forms.CharField(label='Birth date',max_length=30,widget=forms.Textarea,validators=[validateDate])
	gender = forms.CharField(label='Gender',widget=forms.Textarea, validators=[validateGender])

	class Meta:
		model = User
		fields = ['phone','telegram','birth_date','gender']

   
