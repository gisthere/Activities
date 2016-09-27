from django.db import models
from django.contrib.auth.models import User
from locations.models import Location


# Create your models here.
class User(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15)
    telegram = models.CharField(max_length=30)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
    )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
