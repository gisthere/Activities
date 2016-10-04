from django.conf.urls import url
from . import views


app_name = 'activity'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/', views.create, name='create_activity'),
    url(r'^add/', views.add, name='add_activity')
]
