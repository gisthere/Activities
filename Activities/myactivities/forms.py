from django import forms
from django.contrib.auth.models import User

from activity.models import Activity


class MyActivities(forms.Form):
    user = None
    activities = None
    header = ''
    can_remove = False
    can_join = False

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, label_suffix=None, empty_permitted=False,
                 field_order=None, use_required_attribute=None, user=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                         initial=initial, label_suffix=label_suffix, empty_permitted=empty_permitted,
                         field_order=field_order, use_required_attribute=use_required_attribute)
        self.user = user

    def load_created(self):
        self.activities = list(Activity.objects.filter(organizer=self.user))

    def load_participated(self):
        self.activities = list(Activity.objects.filter(participants=self.user))
