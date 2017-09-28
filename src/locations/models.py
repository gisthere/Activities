import json

from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def to_json(self):
        """ Convert object to JSON """
        return dict(name=self.name, latitude=self.latitude, longitude=self.longitude)

    @staticmethod
    def from_json(json_str):
        """ Create object from JSON """
        data = json.loads(json_str)
        result = Location()
        result.name = data['name']
        result.latitude = data['latitude']
        result.longitude = data['longitude']
        return result

    @staticmethod
    def from_dict(dict):
        """ Create object from values in dictionary """
        result = Location()
        result.name = dict['name'][:100]
        result.latitude = str(dict['latitude'])[:15]
        result.longitude = str(dict['longitude'])[:15]
        return result
