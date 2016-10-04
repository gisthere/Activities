from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validator_forbidden_username(value):
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
        raise ValidationError('This is a reserved word.')


def validator_invalid_username(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def validator_unique_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def validator_unique_username_ignore_case(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=150,
                               validators=[validator_forbidden_username, validator_invalid_username])
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'password', ]

    def clean(self):
        super(LoginForm, self).clean()
        password = self.cleaned_data.get('password')
        return self.cleaned_data


class SignupForm(LoginForm):
    confirm_password = forms.CharField(label='confirm_password', max_length=128, widget=forms.PasswordInput)
    first_name = forms.CharField(label='first name', max_length=30, required=False)
    last_name = forms.CharField(label='last name', max_length=30, required=False)
    email = forms.CharField(label='email', max_length=254, required=False,
                            validators=[validator_unique_email])

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
    message = ''

    def __init__(self, header, message):
        super().__init__()
        self.header = header
        self.message = message
