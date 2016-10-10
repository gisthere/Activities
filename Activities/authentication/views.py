from django.contrib import auth
from django.contrib.auth import authenticate

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render

from .forms import SignupForm, MessageForm, LoginForm


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = LoginForm(data=request.POST, files=request.FILES)
        if not form.is_valid():
            return render(request, 'login.htm', {'form': form})
        # check whether the provided credentials are in database or not
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            form = LoginForm()
            form.message = 'Incorrect username/password'
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    return render(request, 'login.htm', {'form': form})


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'login.htm', {'form': form})
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username, email, password)
            user.save()
            auth.login(request, user)
            form = MessageForm('Successful registration', '/    ')
            return render(request, 'msg.htm', {'form': form})
        except IntegrityError as e:
            form = SignupForm()
            form.message = 'Specified user name is already in use';
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'login.htm', {'form': form})
