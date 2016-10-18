import json
import random
from itertools import chain
from django.shortcuts import render
from django.core import serializers
from django.template import loader
from django.views.generic.list import ListView
from django.db.models import Value, CharField, FloatField
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Activity, ActivityType, ActivityCategory
from django.contrib.postgres.search import TrigramSimilarity

def index(request):
    # get search 't' - type and 'v' value 
    if 't' in request.GET and 'v' in request.GET:
        filter_type = request.GET['t']
        filter_value = request.GET['v']

        # check possible variation to prevent XSS injection
        if filter_type == 'at': 
            result = Activity.objects.filter(activity_type = filter_value)
        elif filter_type == 'ac':
            result = Activity.objects.filter(activity_category = filter_value)
        elif filter_type == 'an':
            result = Activity.objects.annotate(
                similarity = TrigramSimilarity('name', request.GET['search'])
                ).filter(similarity__gt=0.1)
    else:
        result = Activity.objects

    context = {
        'activities': result.all()
    }

    template = loader.get_template('index.html')
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




def get_hints(request):
    if 'q' not in request.GET:
        return JsonResponse({})

    search = request.GET['q']
    # name__istartswith
    activity_data = Activity.objects.annotate(
        similarity = TrigramSimilarity('name', search),
        f_name = Value('an', output_field=CharField())
    ).filter(similarity__gt=0.1).values('id', 'name', 'similarity', 'f_name')

    activity_type_data = ActivityType.objects.annotate(
        similarity = Value(0.8, output_field=FloatField()),
        f_name = Value('at', output_field=CharField())
    ).filter(name__istartswith=search).values('id', 'name', 'similarity', 'f_name')

    activity_category_data = ActivityCategory.objects.annotate(
        similarity =  Value(0.6, output_field=FloatField()),
        f_name = Value('ac', output_field=CharField())
    ).filter(name__istartswith=search).values('id', 'name', 'similarity', 'f_name')

    # Get top most suitable hint by order by similarity
    hints = sorted(chain(activity_data, activity_type_data, activity_category_data),
        key=lambda x: x['similarity'], reverse=True)

    result = list(hints)

    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type='application/json')
