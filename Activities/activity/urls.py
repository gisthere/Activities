from django.conf.urls import url
from . import views


app_name = 'activity'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'activity/create/', views.create, name='create_activity'),
    url(r'activity/add/', views.add, name='add_activity'),
    url(r'activity/delete', views.delete, name='delete_activity'),
    url(r'activity/dismiss', views.dismiss, name='dismiss_activity')
]
