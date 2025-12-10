from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transactions', views.transactions, name='transaction'),
    path('accounts', views.accounts, name='account'),
    path('wallet', views.wallet, name='wallet'),
    path('investments', views.investments, name='investment'),
]