from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

#import modules for authentication
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='api.index'),
    url(r'^egi_reporting/users/$', views.count_users, name='api.count_users'),
    url(r'^egi_reporting/users/(?P<startdate_str>[^\/]+)$', views.count_users_with_start_date, name='api.count_users_with_start_date'),
    url(r'^egi_reporting/users/(?P<startdate_str>[^\/]+)/(?P<enddate_str>[^\/]+)$', views.count_users_with_start_end_date, name='api.count_users_with_start_end_date'),
]


