from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Subscription, SearchFilter
from activity.models import ActivityType, ActivityCategory


#  Unsubscribe by filter and user
def unsubscribe(request):
    
    return HttpResponse("sasasribe")

#  Subscribe for new activity by filter and user
def subscribe(request):
    if not request.user.is_authenticated():
        return HttpResponse("Sorry, only authorized user can subsribe.", status=403)

    if 'type' in request.POST and 'value' in request.POST and 'search' in request.POST:

        filter_type = request.POST['type']
        filter_value = request.POST['value']
        filter_search = request.POST['search']

        if filter_type == 'at':
            try:
                search_filter = SearchFilter.objects.get(activity_type = ActivityType.objects.get(id=filter_value))
            except:
                search_filter = SearchFilter.objects.create(activity_type=ActivityType.objects.get(pk=filter_value))
                search_filter.save()

        elif filter_type == 'ac':
            try:
                search_filter = SearchFilter.objects.get(activity_category = ActivityCategory.objects.get(id=filter_value))
            except:
                search_filter = SearchFilter.objects.create(activity_category=ActivityCategory.objects.get(pk=filter_value))
                search_filter.save()
        
        elif filter_type == 'an':
            try:
                search_filter = SearchFilter.objects.get(search=filter_value)
            except:
                search_filter = SearchFilter.objects.create(search=filter_search)
                search_filter.save()

        try:
            subscription = Subscription.objects.get(search_filter = search_filter, user = request.user)
        except:
            subscription = Subscription.objects.create(search_filter = search_filter, user = request.user)
            subscription.save()

    return HttpResponse("subscribe")
