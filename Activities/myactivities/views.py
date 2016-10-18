from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyActivities

""" This file contains function which are used to maintain activities which I have created and
in which I have participated """


def created(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    form = MyActivities(data=request.POST, user=user)
    form.header = 'Organizer'
    form.can_remove = True
    form.load_created()
    return render(request, 'activities.htm', {'form': form})


def participated(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    form = MyActivities(data=request.POST, user=user)
    form.header = 'Participator'
    form.can_join = True
    form.load_participated()
    return render(request, 'activities.htm', {'form': form})
