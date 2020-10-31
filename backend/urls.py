from django.contrib import admin
from django.urls import path, include
from djoser import urls


urlpatterns = [
    path('', include('main.urls')), 
    path('', include('djoser.urls.authtoken'))
]
