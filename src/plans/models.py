from django.contrib.auth.models import User
from django.db import models
from activity.models import ActivityCategory
from activity.models import ActivityType
from activity.models import Activity
from locations.models import Location


# Create your models here.
class PlannedActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description


class Confirmation(models.Model):
    CREATED = 'CR'
    CONFIRMED = 'CO'
    REJECTED = 'RE'
    TYPES = (
        (CREATED, 'Created'),
        (CONFIRMED, 'Confirmed'),
        (REJECTED, 'Rejected'),
    )

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    planned_activity = models.ForeignKey(PlannedActivity, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=TYPES,
        default=CREATED,
    )
