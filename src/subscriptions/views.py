from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Subscription, SearchFilter
from activity.models import ActivityType, ActivityCategory

from django_nyt.utils import notify, subscribe


def subscribeu(request):
    if not request.user.is_authenticated():
        return HttpResponse("not authoride")

    from django_nyt.models import Settings
    settings = Settings.get_default_setting(request.user)
    subscribe(settings, "test")

    return HttpResponse("Ok")


def notifyu(request):
    if not request.user.is_authenticated():
        return HttpResponse("not authoride")

    notify(
        "hello",
        "test",
        target_object=request.user,
    )

    return HttpResponse("OK")


#  Unsubscribe by filter and user
def unsubscribe_on_filter(request, subscription_id):
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, only authorized user can unsubscribe.", status=403)

    try:
        subscription = Subscription.objects.get(id=subscription_id,user=request.user)
        subscription.delete()

        return HttpResponse("subscription was delete")
    except:
        return HttpResponse("can't found", status=404)


#  Subscribe for new activity by filter and user
def subscribe_on_filter(request):
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, only authorized user can subscribe.", status=403)

    if 'type' in request.POST \
            and 'value' in request.POST \
            and 'search' in request.POST:

        filter_type = request.POST['type']
        filter_value = request.POST['value']
        filter_search = request.POST['search']

        if filter_type == 'at':
            s_filter = SearchFilter.objects.get_or_create(activity_type=ActivityType.objects.get(id=filter_value))

        elif filter_type == 'ac':
            s_filter = SearchFilter.objects.get_or_create(
                activity_category=ActivityCategory.objects.get(id=filter_value))

        elif filter_type == 'an':
            s_filter = SearchFilter.objects.get_or_create(search=filter_search)

        if s_filter[1]:
            s_filter[0].save()

        subscription = Subscription.objects.get_or_create(search_filter=s_filter[0], user=request.user)
        if subscription[1]:
            subscription[0].save()

    return HttpResponse("")
