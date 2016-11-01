from django import forms
from django.core.exceptions import ValidationError
from activity.models import Activity
from django.utils.timezone import utc
import datetime


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ActivityForm(forms.ModelForm):
    title = 'Create a new activity'
    id = forms.IntegerField(widget=forms.HiddenInput)
    start_time = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d %H:%i'], widget=DateTimeInput)
    end_time = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d %H:%i'], widget=DateTimeInput)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'requirements', 'start_time', 'end_time', 'participants_limit',
                  'locations',
                  'activity_category', 'activity_type']
        error_messages = {'required': 'This field is required'}

    def clean(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is None:
            start_time = datetime.datetime.utcnow().replace(tzinfo=utc)
            return self.cleaned_data
        if start_time <= datetime.datetime.utcnow().replace(tzinfo=utc):
            raise ValidationError("You can't choose past time, please choose correct one.")
        if start_time > self.cleaned_data.get('end_time'):
            raise ValidationError("Activity can't end before starting, please choose correct dates.")
        if self.cleaned_data.get('participants_limit') <= 0:
            raise ValidationError("At least one participant is required.")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['name'].widget.attrs['placeholder'] = 'title'
        self.fields['description'].widget.attrs['placeholder'] = 'description'
        self.fields['requirements'].widget.attrs['placeholder'] = 'requirements'
        self.fields['participants_limit'].widget.attrs['placeholder'] = 'required participants (not counting yourself)'
        self.fields['activity_type'].widget.attrs['id'] = 'create_form_activity_type'
