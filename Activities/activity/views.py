from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Activity
# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    activities = Activity.objects.all()
    context = {
        'activities': activities
    }
    return HttpResponse(template.render(context, request))

