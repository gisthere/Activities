from django.contrib import admin

from .models import Activity
from .models import ActivityType
from .models import ActivityCategory
from .models import ActivityLocation
from .models import Participant

admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(ActivityCategory)
admin.site.register(ActivityLocation)
admin.site.register(Participant)