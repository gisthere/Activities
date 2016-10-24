from django.http import HttpResponse, HttpResponseRedirect
from .models import Activity, ActivityType, ActivityCategory, ActivityLocation, Participant
import json
from django.core.serializers.json import DjangoJSONEncoder


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
		start_time_mean += datetimeToTotalMinutes(act.start_time) 
		end_time_mean += datetimeToTotalMinutes(act.end_time)


	start_time_mean = start_time_mean / activities.count()
	end_time_mean = end_time_mean / activities.count()

	j_act_value = json.dumps(list(activities.all().values_list('id', 'name', 'start_time','end_time')), cls=DjangoJSONEncoder)
	j_time_value = str(start_time_mean) + "_" + str(end_time_mean)

	result_json = '{"activities":' + j_act_value + ',"times":"' + j_time_value +'"}'

	return HttpResponse(result_json, content_type='application/json')


def datetimeToTotalMinutes(value):
	return (value.hour * 60) + (value.minute)



