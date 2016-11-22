from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from activity.models import Activity, Participant
from authentication.models import User as MUser
from .forms import UserSettingsForm
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    user = request.user
    template = loader.get_template('cabinet.htm')
    # If the 'Profile' page was requested
    if request.method == 'GET':
        data = MUser.objects.get_or_create(user=user)[0]
        form = UserSettingsForm(initial={
            'first_name': '' if user.first_name is None else user.first_name,
            'last_name': '' if user.last_name is None else user.last_name,
            'email': '' if user.email is None else user.email,
            'phone': '' if data.phone is None else data.phone,
            'telegram': '' if data.telegram is None else data.telegram,
            'birth_date': '' if data.birth_date is None else data.birth_date.isoformat(),
            'gender': '' if data.gender is None else data.gender
        })
        return HttpResponse(template.render({'settings_form': form}, request))

    if request.method == 'POST':
        form = UserSettingsForm(data=request.POST)
        if form.is_valid():
            try:
                User.objects.filter(pk=user.pk).update(
                    first_name=None if form.cleaned_data['first_name'] == '' else form.cleaned_data['first_name'],
                    last_name=None if form.cleaned_data['last_name'] == '' else form.cleaned_data['last_name'],
                    email=None if form.cleaned_data['email'] == '' else form.cleaned_data['email'])
                MUser.objects.filter(pk=MUser.objects.get(user=user).pk).update(
                    phone=None if form.cleaned_data['phone'] == '' else form.cleaned_data['phone'],
                    telegram=None if form.cleaned_data['telegram'] == '' else form.cleaned_data['telegram'],
                    birth_date=None if form.cleaned_data['birth_date'] == '' else form.cleaned_data['birth_date'],
                    gender=None if form.cleaned_data['gender'] == '' else form.cleaned_data['gender'])
                return HttpResponseRedirect('/cabinet')
            except Exception as e:
                print(e)
    # return 400
    return HttpResponse(template.render({'settings_form': form}, request))

def user_detail(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    try:
        user = User.objects.get(id = user_id)
        user_info = MUser.objects.get_or_create(user = user)
        participated = Activity.objects.filter(participants = user)
        organized = Activity.objects.filter(organizer = user)
    except MUser.DoesNotExist:
        raise Http404("The user your are looking for doesn't exist.")
    return render(request, 'user_detail.html', {'user_info': user_info, 'user': user, 'participated': participated, 'organized': organized})
