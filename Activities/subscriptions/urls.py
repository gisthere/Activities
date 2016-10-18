from django.conf.urls import url
from . import views

app_name = 'subscriptions'
urlpatterns = [
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
]
