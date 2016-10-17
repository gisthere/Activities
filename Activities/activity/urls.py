from django.conf.urls import url
from . import views


app_name = 'activity'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activity/create/$', views.create, name='activity_create'),
    url(r'^activity/(?P<activity_id>\d+)/$', views.detail, name='activity_detail'),
    url(r'^activity/(?P<pk>\d+)/edit$', views.detail, name='activity_edit'),
    url(r'^activity/(?P<pk>\d+)/delete$', views.detail, name='activity_delete')
]
