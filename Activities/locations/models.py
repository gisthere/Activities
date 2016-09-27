from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)

    def __str__(self):
        return self.name
