from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('accountform', views.account_form, name = 'account_form'),
]