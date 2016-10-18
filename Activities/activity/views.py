from django.db.models import Model
from django.shortcuts import render

from django.template import loader
from django.template.defaulttags import register
from django.http import HttpResponse, HttpResponseRedirect
from .models import Activity, ActivityType, ActivityCategory


# Create your views here.
def index(request):
    types = ActivityType.objects.order_by('id')[:10]
    categories = ActivityCategory.objects.order_by('id')[:10]
    template = loader.get_template('index.html')
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
    return HttpResponse(template.render(context, request))

def calcAvailableSpots(activities):
    availableSpots = {}
    for activity in activities:
        availableSpots[activity.id] = activity.participants_limit - Participant.objects.filter(activity=activity).count()
    return availableSpots

def create(request):
    activity_categories = ActivityCategory.objects.all()
    activity_types = ActivityType.objects.all()
    context = {
        'activity_categories': activity_categories,
        'activity_types': activity_types,
    }
    return render(request, 'activity/create.html', context)


def add(request):
    name = request.POST['name']
    description = request.POST['description']
    requirements = request.POST['requirements']
    participants_limit = request.POST['participants_limit']
    activity_category_id = request.POST['activity_category']
    activity_type_id = request.POST['activity_type']
    activity = Activity(name=name, description=description, status='SC', requirements=requirements,
                        participants_limit=participants_limit,
                        activity_category=ActivityCategory.objects.get(pk=activity_category_id),
                        activity_type=ActivityType.objects.get(pk=activity_type_id))
    activity.save()
    # temp solution, should show my activities
    return HttpResponseRedirect('/')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def delete(request):
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
