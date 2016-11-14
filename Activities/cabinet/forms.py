import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validator_email(value):
    """ Email validator. Throws an exception in case if not valid email was provided. """
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        raise ValidationError('Incorrect Email')


def validate_phone(phone):
    if not re.match(r'^[0-9]{11}$', phone):
        raise ValidationError('Incorrect Phone')


def validate_telegram(telegram):
    if not re.match(r'^\@{1}[a-z,A-Z,0-9,_]*$', telegram):
        raise ValidationError('Incorrect Telegram')


def validate_date(date):
    if not re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', date):
        raise ValidationError('Incorrect Date')


def validate_gender(gender):
    if not (gender == 'F' or gender == 'M'):
        raise ValidationError('Incorrect Gender')


class UserSettingsForm(forms.Form):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = ((MALE, 'Male'), (FEMALE, 'Female'))

    title = 'User profile'
    first_name = forms.CharField(label='First name', max_length=30, required=False)
    last_name = forms.CharField(label='Last name', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=False, validators=[validator_email])
    phone = forms.CharField(label='Phone', max_length=11, required=False, validators=[validate_phone])
    telegram = forms.CharField(label='Telegram', max_length=30, required=False, validators=[validate_telegram])
    birth_date = forms.CharField(label='Birth date', max_length=30, required=False, validators=[validate_date])
    gender = forms.ChoiceField(choices=GENDER, required=False, widget=forms.Select(attrs={'class' : 'form-control'}))

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'phone', 'telegram', 'birth_date', 'gender']
