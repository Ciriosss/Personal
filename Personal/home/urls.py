from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.financeDashboard, name = 'financeDashboard'),
    path('fitnessDasboard/', views.fitnessDashboard, name = 'fitnessDashboard'),
    path('habitsDashboard/', views.habitsDashboard, name = 'habitsDashboard'),
    path('toDoDashboard/', views.toDoDashboard, name = 'toDoDashboard'),
    path('projectsDashboard/', views.projectsDashboard, name = 'projectsDashboard'),
]
