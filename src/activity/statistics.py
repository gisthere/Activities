from django.http import HttpResponse, HttpResponseRedirect
from .models import Activity, ActivityType, ActivityCategory, ActivityLocation, Participant
from django.template import loader

def recommendations(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	ac_id = request.GET.get('type')

	activities = Activity.objects.filter(activity_type=ActivityType.objects.get(id=ac_id))
	start_time_mean = 0;
	end_time_mean = 0;

	if activities.count() == 0 or ac_id is None:
		return HttpResponse();


	for act in activities:
		start_time_mean += act.start_time.hour
		end_time_mean += act.end_time.hour

	template = loader.get_template('activity/activities_reccomendation.html')


	start_time_mean = start_time_mean / activities.count()
	end_time_mean = end_time_mean / activities.count()

	if end_time_mean < start_time_mean :
		end_time_mean = start_time_mean + 1
	context = {
    	'activities' : activities.all(),
    	'time_from_rec' : "%.0f" % start_time_mean,
    	'time_to_rec' : "%.0f" % end_time_mean
    }

	return HttpResponse(template.render(context, request))

