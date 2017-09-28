from django.conf.urls import url
from . import views

app_name = 'subscriptions'
urlpatterns = [
    url(r'^unsubscribe/(?P<subscription_id>\d+)/$', views.unsubscribe_on_filter, name='unsubscribe'),
    url(r'^subscribe/$', views.subscribe_on_filter, name='subscribe'),
    url(r'^notify/$', views.notifyu, name='notifyuse'),
    url(r'^subscribeu/$', views.subscribeu, name='subscribeu'),

]
