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

class UserSettingsForm(forms.Form):
	title = 'User settings'
	phone = forms.CharField(label='Phone', max_length=11, widget=forms.Textarea, validators=[validatePhone])
	telegram = forms.CharField(label='Telegram',max_length=30,widget=forms.Textarea,validators=[validateTelegram])
	birth_date = forms.DateField(label='Birth date')
	genders = (('F','FEMALE'),('M','MALE'))
	gender = forms.ChoiceField(choices=genders)

	class Meta:
		model = User
		fields = ['phone','telegram','birth_date','gender']

   
