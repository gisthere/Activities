from django.db import models
from django.contrib.auth.models import User
from activity.models import ActivityCategory, ActivityType


# Create your models here.

class SearchFilter(models.Model):
    activity_type = models.ForeignKey(ActivityType, null=True)
    activity_category = models.ForeignKey(ActivityCategory, null=True)
    search = models.CharField(max_length=50, null=True)


class Subscription(models.Model):
    search_filter = models.ForeignKey(SearchFilter, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# class SearchFilterManager(models.Manager):

#     def get_or_create(self, activity_type, activity_category, fuzze_search):


#         return filter


# class SubscriptionsManager(models.Manager):

#      def subscribe(self, filter, user):
