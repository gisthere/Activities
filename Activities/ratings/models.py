from django.db import models
from django.contrib.auth.models import User
from activity.models import Activity


# Class represents single rating and commend left by ORGANIZATOR of ACTIVITY for SINGLE PARTICIPANT
class SingleParticipantRating(models.Model):
	activity = models.ForeignKey(Activity, on_delete=models.SET_NULL,null=True)
	rated_user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
	rating = models.PositiveSmallIntegerField(null=True)
	comment = models.TextField()