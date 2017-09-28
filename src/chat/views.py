from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Chat
from activity.models import Activity
from django.contrib.auth.models import User
# from .forms import ChatForm


# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    template = loader.get_template('chat/index.html')

    loggedUser = None


    if request.method == 'POST':
        if 'UserMessage' in request.POST:
            msgText = request.POST['UserMessage']
            userName = request.user
            activ = Activity.objects.get(id = 1)

            newComment = Chat.objects.create(user = request.user, activity = activ, message = msgText)
            newComment.save()


    userprofile = request.user
    activ = Activity.objects.get(id = 1)
    allComments = Chat.objects.filter(activity = activ)
    # form = ChatForm()
    # allComments = Chat.objects.all()
    context = {
        'title' : activ,
        'comments': allComments,
        'currentUser': userprofile,
        # 'activity_form': form
    }

    result = template.render(context, request)
    return HttpResponse(result)


    # if request.user.is_authenticated():
    #     organizer = User.objects.get(id=request.user.id)
    #     activities = Activity.objects.filter(organizer=organizer)
    #     if request.method == 'GET':
    #         if activity_id is not None:
    #             activity = Activity.objects.get(id=activity_id)
    #             form = ActivityForm(instance=activity)
    #         else:
    #             form = ActivityForm()
    #     else:
    #         form = ActivityForm(request.POST)
    #         if form.is_valid():
    #             activity = form.save(commit=False)
    #             activity.organizer = request.user
    #             activity.save()
    #             return HttpResponseRedirect(reverse('activity:activity_detail', kwargs={'activity_id': activity.id}))
    #     return render(request, 'activity/create.html', {'activity_form': form, 'activities': activities})
    # else: