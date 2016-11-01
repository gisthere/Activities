from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(name=self.name, latitude=self.latitude, longitude=self.longitude)
