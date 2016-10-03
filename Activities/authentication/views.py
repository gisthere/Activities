from django.contrib import auth
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render

# from django.http import HttpResponseRedirect
from .forms import SignupForm, MessageForm, LoginForm


def login(request):
    if request.user.is_authenticated():
        form = MessageForm('Authorized', 'You are authorized already')
        return render(request, 'msg.htm', {'form': form})
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
            form = MessageForm('Success', 'Successful authorization')
            return render(request, 'msg.htm', {'form': form})
        else:
            form = MessageForm('Error', 'unknown user')
            return render(request, 'msg.htm', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.htm', {'form': form})


def signup(request):
    if request.user.is_authenticated():
        form = MessageForm('Authorized', 'You are authorized already')
        return render(request, 'msg.htm', {'form': form})
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'signup.htm', {'form': form})
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username, email, password)
            user.save()
            auth.login(request, user)
            form = MessageForm('Success', 'Successful registration')
            return render(request, 'msg.htm', {'form': form})
        except IntegrityError as e:
            form = MessageForm('Error', 'Specified username is already in use.')
            return render(request, 'msg.htm', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'signup.htm', {'form': form})
