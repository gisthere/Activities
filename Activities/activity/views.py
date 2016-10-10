from django.shortcuts import render

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Activity, ActivityType, ActivityCategory
# Create your views here.
def index(request):
    types = ActivityType.objects.order_by('id')[:10]
    categories = ActivityCategory.objects.order_by('id')[:10]
    template = loader.get_template('index.html')
    if 'activity_type' in request.GET and request.GET['activity_type'].strip():
        query = request.GET['activity_type']

        activities = Activity.objects.filter(activity_type=query)
    else:
        activities = Activity.objects.all()
    context = {
        'activities': activities,
        'types': types,
        'categories': categories
    }
    return HttpResponse(template.render(context, request))


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
    activity = Activity(name=name, description=description, status='SC', requirements=requirements, participants_limit=participants_limit, activity_category=ActivityCategory.objects.get(pk=activity_category_id), activity_type=ActivityType.objects.get(pk=activity_type_id))
    activity.save()
    #temp solution, should show my activities
    return HttpResponseRedirect('/')
