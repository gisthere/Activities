import json
import random
import datetime
from itertools import chain

from django.contrib.auth.models import User
from django.db.models import Model, Count, Sum, Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from authentication.models import User as MUser
from django.views.generic import ListView

from .models import Activity, ActivityType, ActivityCategory, ActivityLocation, Participant
from chat.models import Chat
from .forms import ActivityForm
from django.template import loader
from django.template.defaulttags import register
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Value, CharField, FloatField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class ActivityList(ListView):
    model = Activity
    paginate_by = 10
    context_object_name = 'activities'
    template_name = 'activity/activities_list.html'



    def get_queryset(self):
        list = Activity.objects.annotate(
            num_participant=Count('participant'),
            rating =Avg('participant__rating')
        )

        # get search 't' - type and 'v' value
        if 't' in self.request.GET and 'v' in self.request.GET and self.request.GET['t']:
            filter_type = self.request.GET['t']
            filter_value = self.request.GET['v']

            # check possible variation to prevent XSS injection
            if filter_type == 'at':
                result = list.filter(activity_type=filter_value)
            elif filter_type == 'ac':
                result = list.filter(activity_category=filter_value)
            elif filter_type == 'an':
                result = list.annotate(
                    similarity=TrigramSimilarity('name', self.request.GET['search'])
                ).filter(similarity__gt=0.1)

            if result:
                self.page_kwarg = 0
        else:
            result = list

        activities = result.all()
        for activity in activities:
            activity.available_spots = activity.participants_limit - activity.num_participant

        if 'order_by' in self.request.GET and self.request.GET['order_by']:
            if self.request.GET['order_by'] == 'rating':
                return activities.order_by('-rating')
            else:
                return activities.order_by('start_time')
        else:
            return activities


# Create your views here.
def index(request):
    # get search 't' - type and 'v' value 
    if 't' in request.GET and 'v' in request.GET:
        filter_type = request.GET['t']
        filter_value = request.GET['v']
        latitude = None
        longitude = None
        # extract GEO information from the search request
        if 'lat' in request.GET:
            try:
                distance = float(request.GET['distance'])
                latitude = float(request.GET['lat'])
                longitude = float(request.GET['lng'])
            except ValueError as e:
                latitude = None
                longitude = None
        if latitude is None or longitude is None:
            try:
                usr = MUser.objects.get(user=request.user)
                longitude = float(usr.location.longitude)
                latitude = float(usr.location.latitude)
            except Exception as e:
                print(e)
        # check possible variation to prevent XSS injection
        if filter_type == 'at':
            result = Activity.objects.filter(activity_type=filter_value)
        elif filter_type == 'ac':
            result = Activity.objects.filter(activity_category=filter_value)
        elif filter_type == 'an':
            result = Activity.objects.annotate(
                similarity=TrigramSimilarity('name', request.GET['search'])
            ).filter(similarity__gt=0.1)
        # use GEO information of the search request if there was any
        objs = result.filter(status='SC',start_time__gte=datetime.date.today()).all()
        if latitude is not None or longitude is not None:
            res = []
            latScale = 111  # value in kilometers
            lngScale = 111  # value in kilometers
            # output only activities which located no further than 'distance' threshold
            for activity in objs:
                # if at least one location of the activity is located within
                # the specified distance, then add it to the output list
                locs = activity.activitylocation_set.all()
                if len(locs) == 0:
                    res.append(activity)
                else:
                    for loc in locs:
                        lat = float(loc.location.latitude)
                        lng = float(loc.location.longitude)
                        dist = pow((lat - latitude) * latScale, 2.0) \
                               + pow((lng - longitude) * lngScale, 2.0)
                        dist = pow(dist, 0.5)
                        if dist <= distance:
                            res.append(activity)
                            break
            objs = res
    else:
        if request.user.is_authenticated():
            objs = Activity.objects.filter(status='SC',start_time__gte=datetime.date.today()).exclude(participants=request.user).all()
        else:
            objs = Activity.objects.filter(status='SC',start_time__gte=datetime.date.today()).all()
    availableSpots = calcAvailableSpots(Activity.objects.all())
    context = {
        'user': request.user,
        'activities': objs,
        'availableSpots': availableSpots
    }
    template = loader.get_template('activity/index.html')
    return HttpResponse(template.render(context, request))


def get_hints(request):
    if 'q' not in request.GET:
        return JsonResponse({})

    search = request.GET['q']
    # name__istartswith
    activity_data = Activity.objects.annotate(
        similarity=TrigramSimilarity('name', search),
        f_name=Value('an', output_field=CharField())
    ).filter(similarity__gt=0.1).values('id', 'name', 'similarity', 'f_name')

    activity_type_data = ActivityType.objects.annotate(
        similarity=Value(0.8, output_field=FloatField()),
        f_name=Value('at', output_field=CharField())
    ).filter(name__istartswith=search).values('id', 'name', 'similarity', 'f_name')

    activity_category_data = ActivityCategory.objects.annotate(
        similarity=Value(0.6, output_field=FloatField()),
        f_name=Value('ac', output_field=CharField())
    ).filter(name__istartswith=search).values('id', 'name', 'similarity', 'f_name')

    # Get top most suitable hint by order by similarity
    hints = sorted(chain(activity_data, activity_type_data, activity_category_data),
                   key=lambda x: x['similarity'], reverse=True)

    result = list(hints)

    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type='application/json')


def locations(request, activity_id):
    #  redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # do nothing if there is no valid info in request
    if activity_id is None:
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        a = activity.activitylocation_set.all()
        result = [obj.to_json() for obj in activity.activitylocation_set.all()]
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json')
    except Exception as e:
        print(e)
    return HttpResponse()


def calcAvailableSpots(activities):
    availableSpots = {}
    for activity in activities:
        availableSpots[activity.id] = activity.participants_limit - Participant.objects.filter(
            activity=activity).count()
    return availableSpots


def create(request, activity_id=None):
    if request.user.is_authenticated():
        organizer = User.objects.get(id=request.user.id)
        activities = Activity.objects.filter(organizer=organizer)
        if request.method == 'GET':
            if activity_id is not None:
                activity = Activity.objects.get(id=activity_id)
                form = ActivityForm(instance=activity)
                form.title = 'Copy from activity'
            else:
                form = ActivityForm()
                form.title = 'Create a new activity'
        else:
            data = request.POST['locations']
            locs = ActivityLocation.from_json(data)
            post = request.POST.copy()
            # remove extra information concerning the locations
            post.pop('locations')
            form = ActivityForm(post)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.organizer = request.user
                activity.save()
                # save locations into database
                for loc in locs:
                    loc.activity = activity
                    loc.location.save()
                    loc.location_id = loc.location.id
                    loc.save()
                # basic trigger notification system on creating new activity
                activity.notify_subscribers()
                # end basic trigger notifiaction system
                return HttpResponseRedirect(reverse('activity:activity_detail', kwargs={'activity_id': activity.id}))
            print(form.errors)
        return render(request, 'activity/create.html', {'activity_form': form, 'activities': activities})
    else:
        return HttpResponseRedirect('login/')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# Delete activity by specified id (passed as get parameter)
def delete(request, activity_id):
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        # restrict deletion in case if activity does not belong to the user
        # or if was already performed
        if activity.organizer.id != request.user.id or activity.status == 'PF':
            return HttpResponse()
        activity.delete()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


# Dismiss activity by specified activity id and user id (passed as get parameters)
def dismiss(request, activity_id):
    # redirect to main page if the user is not authenticated
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    # do nothing if there is no valid info in request
    if activity_id is None:
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        part_activity = Participant.objects.get(user=user, activity=activity)
        part_activity.delete()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


# Join activity by specified activity id and user id (passed as get parameters)
def join(request):
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    activity_id = request.GET.get('activity_id')
    user_id = request.GET.get('user_id')
    if user_id is None:
        return HttpResponseRedirect('/signup')
    # do nothing if there is no valid info in request
    if activity_id is None:
        return HttpResponse()
    try:
        # try to load activity from the database
        user = User.objects.get(id=user_id)
        activity = Activity.objects.get(id=activity_id)

        if user in activity.participants.all():
            return HttpResponseRedirect('/')
        
        Participant.objects.update_or_create(user=user, activity=activity)
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


# Checks whether the provided status is valid
def validate_status(new_status):
    valid_status = False
    for status in Activity.STATUSES:
        if new_status == status[0]:
            valid_status = True
            break
    return valid_status


# Change status of the activity by specified activity id and new status value (passed as get parameters)
def change_status(request, activity_id, new_status):
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # do nothing if there is no valid info in request
    if activity_id is None or new_status is None:
        return HttpResponse()
    # check whether the provided status is valid
    if not validate_status(new_status):
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        activity.status = new_status
        activity.save()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


# Change rating of the activity by specified activity id and new rating value (passed as get parameters)
def change_rating(request, activity_id, new_rating):
    # redirect to main page if the user is not authenticated
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    # do nothing if there is no valid info in request
    if activity_id is None or new_rating is None:
        return HttpResponse()
    # check whether the provided rating is valid
    new_rating = int(new_rating)
    if new_rating < 0 or new_rating > 5:
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        # set the rating from the participant
        participation = Participant.objects.get_or_create(user=user, activity=activity)[0]
        participation.rating = new_rating
        participation.save()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


def change_participant_rating(request, activity_id, participant_id, new_rating):
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # do nothing if there is no valid info in request
    if activity_id is None or participant_id is None or new_rating is None:
        return HttpResponse()
    # check whether the provided rating is valid
    new_rating = int(new_rating)
    if new_rating < 0 or new_rating > 5:
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        if request.user.id == activity.organizer_id:
            participant = User.objects.get(id=participant_id)
            print(participant.first_name)
            # set the rating from the participant
            participation = Participant.objects.get_or_create(user=participant, activity=activity)[0]
            participation.participant_rating = new_rating
            participation.save()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse(participation.total_rating)

# Add comment for participant
def add_comment_for_participant(request,activity_id, participant_id):
    # redirect to main page if the user is not authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if 'comment' in request.POST:
        comment  = request.POST['comment']
    # do nothing if there is no valid info in request
    if activity_id is None or participant_id is None or comment is None:
        return HttpResponse()
    # check whether the provided rating is valid
    if not comment:
        return HttpResponse()
    try:
        # try to load activity from the database
        activity = Activity.objects.get(id=activity_id)
        participant = User.objects.get(id=participant_id)
        print(participant.first_name)
        # set the rating from the participant
        participation = Participant.objects.get_or_create(user=participant, activity=activity)[0]
        participation.comment_for_participant = comment
        participation.save()
    except Model.DoesNotExist as e:
        print(e)
    return HttpResponse()


def detail(request, activity_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    try:
        activity = Activity.objects.get(pk=activity_id)
        participants = Participant.objects.filter(activity=activity)
        if request.method == 'POST':
            if 'UserMessage' in request.POST:
                msgText = request.POST['UserMessage']
                activ = Activity.objects.get(id = activity_id)
                newComment = Chat.objects.create(user = request.user, activity = activ, message = msgText)
                newComment.save()
        activ = Activity.objects.get(id = activity_id)
        allComments = Chat.objects.filter(activity = activ)
    except Activity.DoesNotExist:
        raise Http404("The activity your are looking for doesn't exist.")
    return render(request, 'activity/detail.html', {'activity': activity, 'comments': allComments, 'participants': participants})


def edit(request, activity_id=None):
    if request.user.is_authenticated():
        try:
            activity = Activity.objects.get(id=activity_id)
            if request.method == 'GET':
                form = ActivityForm(instance=activity)
                form.title = 'Edit the activity'
                return render(request, 'activity/edit.html', {'activity_form': form})
            else:
                data = request.POST['locations']
                locs = ActivityLocation.from_json(data)
                post = request.POST.copy()
                # remove extra information concerning the locations
                post.pop('locations')
                form = ActivityForm(post, instance=activity)
                if form.is_valid():
                    activity = form.save(commit=False)
                    activity.organizer = request.user
                    activity.save()
                    # save locations into database
                    for loc in locs:
                        loc.activity = activity
                        loc.location.save()
                        loc.location_id = loc.location.id
                        loc.save()
                    return HttpResponseRedirect(
                        reverse('activity:activity_detail', kwargs={'activity_id': activity.id}))
        except Activity.DoesNotExist:
            raise Http404("The activity your are looking for doesn't exist.")
    else:
        return HttpResponseRedirect('login/')
