from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Chat
from activity.models import Activity
from authentication.models import User


# Create your views here.

def index(request):
    comments = Chat.objects.order_by('id')[:5]
    template = loader.get_template('chat/index.html')
    context = {
        'comments1': comments,
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))

def send_Comment(request):
	if request.method == 'POST':
		
		userComment = request.POST.get('UserMessage')
		activ = Activity.objects.get(id = 1)

		user = request.user

		userprofile = User.objects.get(user = user)
		comment = Chat.objects.create(user = userprofile, activity = activ, message = userComment)
		comment.save()
		# return HttpResponse(template.render)
		return HttpResponse('HALLE')


	return HttpResponse('message')
		# models.add
    # 
