from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
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

