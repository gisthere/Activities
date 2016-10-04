from django.shortcuts import render

from .models import Activity
from .models import ActivityCategory
from .models import ActivityType


def index(request):
    activities = Activity.objects.all().order_by("-start_time")[:10]
    context = {
        'activities': activities
    }
    return render(request, 'activity/index.html', context)


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
    return render(request, 'activity/index.html')
