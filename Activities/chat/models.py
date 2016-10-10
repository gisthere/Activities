from __future__ import unicode_literals

from django.db import models
from authentication.models import User
from activity.models import Activity

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)  
    message = models.CharField(max_length=500, null = True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank = True, null = True)
