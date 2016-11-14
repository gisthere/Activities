from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from authentication.models import User
from .forms import UserSettingsForm
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	logged_user = request.user

	try:
		logged_user_data = User.objects.get(user=logged_user)
	except ObjectDoesNotExist:
		User.objects.create(user=logged_user,birth_date='2000-01-01')
		logged_user_data = User.objects.get(user=logged_user)

	if request.method == 'GET':

		template = loader.get_template('cabinet/index.html')

		settings_form = UserSettingsForm(initial={
			'phone'			: logged_user_data.phone,
			'telegram' 		: logged_user_data.telegram,
			'birth_date' 	: logged_user_data.birth_date.isoformat(),
			'gender'		: logged_user_data.gender
			})

		context = {
			'settings_form' : settings_form
		}

		return HttpResponse(template.render(context, request))

	if request.method == 'POST':

		settings_form = UserSettingsForm(data=request.POST)

		if settings_form.is_valid():
			User.objects.filter(pk=User.objects.get(user=logged_user).pk).update(
				phone		=settings_form.cleaned_data['phone'],
				telegram	=settings_form.cleaned_data['telegram'],
				birth_date	=settings_form.cleaned_data['birth_date'],
				gender		=settings_form.cleaned_data['gender']
			)
			return HttpResponseRedirect('/cabinet')

	#return 400
	return HttpResponseRedirect('/cabinet')		



