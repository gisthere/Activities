from django.db import models
from activity.models import Activity
from django.contrib.auth.models import User

class SingleParticipantRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
	activity = models.ForeignKey(Activity, on_delete=models.SET_NULL,null=True)
	rating = models.PositiveSmallIntegerField(null=True)
	comment = models.TextField()
