from django.db.models import Model
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Activity, ActivityType, ActivityCategory, ActivityLocation, Participant
from .forms import ActivityForm
from django.template import loader
from django.template.defaulttags import register


# Create your views here.
def index(request):
    types = ActivityType.objects.order_by('name')[:10]
    categories = ActivityCategory.objects.order_by('name')[:10]
    template = loader.get_template('activity/index.html')
    availableSpots = calcAvailableSpots(Activity.objects.all())


    if 'activity_type' in request.GET and request.GET['activity_type'].strip():
        query = request.GET['activity_type']
        activities = Activity.objects.filter(activity_type=query)
    else:
        activities = Activity.objects.all()

    context = {
        'availableSpots': availableSpots,
        'activities': activities,
        'types': types,
        'categories': categories
    }
    return render(request, 'activity/index.html', context)


def calcAvailableSpots(activities):
    availableSpots = {}
    for activity in activities:
        availableSpots[activity.id] = activity.participants_limit - Participant.objects.filter(
            activity=activity).count()
    return availableSpots


def create(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            form = ActivityForm()
        else:
            form = ActivityForm(request.POST)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.organizer = request.user
                activity.save()
                return HttpResponseRedirect(reverse('activity:activity_detail', kwargs={'activity_id': activity.id}))
        return render(request, 'activity/create.html', {'activity_form': form})
    else:
        return HttpResponseRedirect('login/')
    # activity_categories = ActivityCategory.objects.all()
    # activity_types = ActivityType.objects.all()
    # context = {
    #     'activity_categories': activity_categories,
    #     'activity_types': activity_types,
    # }
    # return render(request, 'activity/create.html', context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def delete(request):
    print('delete hello activity_id')
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # get the ID from the get request
    activity_id = request.GET.get('id')
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        # restrict deletion in case if activity does not belong to the user
        if activity.organizer.id != request.user.id:
            return HttpResponse()
        activity.delete()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


def detail(request, activity_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
    except Activity.DoesNotExist:
        raise Http404("The activity your are looking for doesn't exist.")
    return render(request, 'activity/detail.html', {'activity': activity})
