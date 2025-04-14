from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transactions', views.transactions, name = 'fin-transactions'),
    path('accounts', views.accounts, name = 'fin-accounts'),
    path('wallet', views.wallet, name = 'fin-wallet'),
    path('investments', views.investments, name = 'fin-investments'),
    path('check', views.check, name = 'fin-check'),

]
