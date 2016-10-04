from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Chat

# Create your views here.

def index(request):
    comments = Chat.objects.order_by('id')[:5]
    template = loader.get_template('chat/index.html')
    context = {
        'comments1': comments,
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse('HALLE')
