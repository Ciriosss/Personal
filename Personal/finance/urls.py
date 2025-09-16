from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transactions', views.transactions, name='transaction'),
    path('accounts', views.transactions, name='account'),
    path('wallet', views.transactions, name='wallet'),
    path('investments', views.transactions, name='investment'),
]