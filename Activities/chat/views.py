from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Chat
from activity.models import Activity
from authentication.models import User


# Create your views here.

def index(request):
    template = loader.get_template('chat/index.html')

    loggedUser = None


    if request.method == 'POST':
        if 'UserMessage' in request.POST:
            msgText = request.POST['UserMessage']
            userName = request.user
            id = request.user
            userprofile = User.objects.get(user = id)
            activ = Activity.objects.get(id = 2)

            newComment = Chat.objects.create(user = userprofile, activity = activ, message = msgText)
            newComment.save()

    allComments = Chat.objects.all
    context = {
        'title' : Chat.objects.get(id = 2).activity,
        'comments': allComments,
        'currentUser': request.user,
    }

    result = template.render(context, request)
    return HttpResponse(result)