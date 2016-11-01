from django.contrib.auth.models import User
from django.db import models
from locations.models import Location


# Create your models here.
class ActivityCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('ActivityCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    SCHEDULED = 'SC'
    CANCELED = 'CN'
    PERFORMED = 'PF'
    STATUSES = (
        (SCHEDULED, 'Scheduled'),
        (CANCELED, 'Canceled'),
        (PERFORMED, 'Performed'),
    )

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=STATUSES,
        default=SCHEDULED,
    )
    requirements = models.TextField()
    comments = models.ManyToManyField(User, through='Comment')
    participants = models.ManyToManyField(User, through='Participant',
                                          related_name='participants_of_activity')
    participants_limit = models.PositiveIntegerField()
    locations = models.ManyToManyField(Location, through='ActivityLocation')
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  related_name='organizer_of_activity')
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def rating(self):
        result = 0
        n = 0
        try:
            for participant in self.participant_set.all():
                if participant.rating is not None:
                    result += participant.rating
                    n += 1
        except Exception as e:
            print(e)
        if n > 0:
            return round(result / n)
        return None


class ActivityLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True)


# perhaps we should move 'Comments' to its own app later
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    comment = models.TextField()
