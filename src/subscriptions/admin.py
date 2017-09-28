from django.contrib import admin
from .models import Subscription, SearchFilter

admin.site.register(Subscription)
admin.site.register(SearchFilter)