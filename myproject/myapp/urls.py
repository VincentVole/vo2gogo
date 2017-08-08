# -*- coding: utf-8 -*-
from django.conf.urls import url
from myproject.myapp.views import list
from . import views

urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^$', views.index),
    url(r'^uploads/$', views.uploads),
    url(r'^custom/$', views.custom)
]
