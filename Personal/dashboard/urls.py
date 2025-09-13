from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('fitness', views.fitness_dashboard, name = 'fitness_dashboard'),

    path('accountform', views.account_form, name = 'account_form'),
    path('transactionform', views.transaction_form, name = 'transaction_form'),
    path('labelform', views.label_form, name = 'label_form'),
    path('investmentform', views.investment_form, name = 'investment_form'),
    path('wallet', views.wallet_form, name = 'wallet_form'),
]