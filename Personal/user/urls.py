from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'user/sign-in.html'), name = 'sign-in'),
    path('sign-up', views.sign_up, name ='sign-up'),
    path('dashboard', include('dashboard.urls')),
    
    
    
]