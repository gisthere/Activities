import json
from django.shortcuts import render
from django.core import serializers
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Activity, ActivityType, ActivityCategory

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
        else:
            result = Activity.objects.filter(name__istartswith = filter_value)
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


def get_search_suggestions(request):
    if 'search' not in request.GET:
        return JsonResponse({})

    query_parameter = request.GET['search']

    result = {}
    types_query = ActivityType.objects.filter(
        name__istartswith=query_parameter
    )

    result = {}
    if types_query.count() < 2:
        categories_query = ActivityCategory.objects.filter(
            name__istartswith=query_parameter
        )
        data = categories_query

        if categories_query.count() != 0:
            result['types'] = 'ac'
        else:
            result['types'] = 'm'
    else:
        data = types_query
        result['types'] = 'at'

    result['data'] = list(data.values())
    qs_json = json.dumps(result),

    return HttpResponse(qs_json, content_type='application/json')
