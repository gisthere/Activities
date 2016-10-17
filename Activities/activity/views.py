from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Activity, ActivityType, ActivityCategory, ActivityLocation
from .forms import ActivityForm


# Create your views here.
def index(request):
    types = ActivityType.objects.order_by('name')[:10]
    categories = ActivityCategory.objects.order_by('name')[:10]
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
    return render(request, 'activity/index.html', context)


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


def detail(request, activity_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
    except Activity.DoesNotExist:
        raise Http404("The activity your are looking for doesn't exist.")
    return render(request, 'activity/detail.html', {'activity': activity})
