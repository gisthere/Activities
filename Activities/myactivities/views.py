from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyActivities

""" This file contains function which are used to maintain activities which I have created and
in which I have participated """


def created(request):
    """ This method returns page with the list of the activities
     created by the current user """
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    form = MyActivities(data=request.POST, user=user)
    form.header = 'Organizer'
    form.can_remove = True
    form.is_created = True
    form.load_created()
    return render(request, 'activities.htm', {'form': form})


def participated(request):
    """ This method return page with the list of the activities
     in which current user enrolled as participant """
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    form = MyActivities(data=request.POST, user=user)
    form.header = 'Participator'
    form.can_join = True
    form.is_created = False
    form.load_participated()
    form.load_rated()
    return render(request, 'activities.htm', {'form': form})
