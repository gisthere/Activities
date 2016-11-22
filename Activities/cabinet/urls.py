from django.conf.urls import url
from . import views


app_name = 'cabinet'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
]
