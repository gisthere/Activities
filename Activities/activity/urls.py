from django.conf.urls import url
from . import views


app_name = 'activity'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'activity/create/', views.create, name='create_activity'),
    url(r'activity/add/', views.add, name='add_activity'),
    url(r'activity/search_suggestions/', views.get_search_suggestions, name='search_suggestions')
]
