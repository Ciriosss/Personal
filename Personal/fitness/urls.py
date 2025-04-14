from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('activity', views.activity, name = 'fit-activity'),
    path('body', views.body, name = 'fit-body'),
    path('performance', views.performance, name = 'fit-performance'),
]
