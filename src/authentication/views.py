from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from authentication.models import User as MUser
from locations.models import Location

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
            update_user_location(request, user)
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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.save()
            auth.login(request, user)
            update_user_location(request, user)
            form = MessageForm('Successful registration', '/')
            return render(request, 'msg.htm', {'form': form})
        except IntegrityError as e:
            form = SignupForm()
            form.message = 'Specified user name is already in use'
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    return render(request, 'login.htm', {'form': form})


def shrink_str(str, max_len):
    str = str.strip()
    if len(str) > max_len:
        return str[0:max_len]
    return str


def update_user_location(request, user):
    longitude = request.POST['longitude']
    latitude = request.POST['latitude']
    if longitude is None or latitude is None:
        return
    longitude = shrink_str(longitude, 15)
    latitude = shrink_str(latitude, 15)
    if len(longitude) == 0 or len(latitude) == 0:
        return
    # get the inner user information
    muser = MUser.objects.get_or_create(user=user)[0]
    if muser.user is None:
        muser.user = user
    # get the last location of the user
    location = muser.location
    if location is None:
        location = Location()
    # assign new location of the user
    location.longitude = longitude
    location.latitude = latitude
    try:
        location.save()
        muser.location = location
        muser.save()
    except Exception as e:
        print(e)
