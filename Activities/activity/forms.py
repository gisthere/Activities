from django import forms
from django.core.exceptions import ValidationError
from activity.models import Activity


class ActivityForm(forms.ModelForm):
    title = 'Create a new activity'

    class Meta:
        model = Activity
        fields = ['name', 'description', 'requirements', 'participants_limit', 'locations',
                  'activity_category', 'activity_type']
        error_messages = {'required': 'This field is required'}

    def clean(self):
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
