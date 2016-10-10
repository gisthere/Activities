import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validator_forbidden_username(value):
    """
    This function is used as a validator of user names.
    It throws an exception in case if some predefined username was used.
    """
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]
    if value.lower() in forbidden_usernames:
        raise ValidationError('This is reserved word')


def validator_invalid_username(value):
    """
    This function throws an exception in case if provided input value
    contains @, +, - symbols.
    """
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username')


def validator_email(value):
    """ Email validator. Throws an exception in case if not valid email was provided. """
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        raise ValidationError('Incorrect Email')


def validator_unique_email(value):
    """ Email validator. Throws an exception if provided email is already in use. """
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists')


def validator_unique_username_ignore_case(value):
    """ Username validator. Throws an exception if provided username is already in use. """
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists')


class LoginForm(forms.Form):
    error_messages = {'required': 'This field is required'}
    title = 'Login'
    action = '/login/'
    switch_title = 'Sign up'
    switch_action = '/signup/'
    message = ''
    username = forms.CharField(label='Username', max_length=150, initial='', error_messages=error_messages,
                               validators=[validator_forbidden_username, validator_invalid_username])
    password = forms.CharField(label='Password', max_length=128, initial='', error_messages=error_messages,
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'password', ]

    def clean(self):
        super(LoginForm, self).clean()
        password = self.cleaned_data.get('password')
        return self.cleaned_data


class SignupForm(LoginForm):
    confirm_password = forms.CharField(label='Confirm password', max_length=128, initial='',
                                       error_messages=LoginForm.error_messages,
                                       widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', max_length=30, initial='', required=False)
    last_name = forms.CharField(label='Last name', max_length=30, initial='', required=False)
    email = forms.EmailField(label='Email', max_length=254, initial='', required=False,
                             validators=[validator_email, validator_unique_email])

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, label_suffix=None,
                 empty_permitted=False, field_order=None, use_required_attribute=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                         initial=initial, label_suffix=label_suffix, empty_permitted=empty_permitted,
                         field_order=field_order, use_required_attribute=use_required_attribute)
        self.title = 'Sign up'
        self.action = '/signup/'
        self.switch_title = 'Login'
        self.switch_action = '/login/'

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'password', 'confirm_password', 'email',
                  'first_name', 'last_name', ]

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data


class MessageForm(forms.Form):
    header = ''
    redirect_url = ''

    def __init__(self, header, redirect_url=''):
        super().__init__()
        self.header = header
        self.redirect_url = redirect_url
