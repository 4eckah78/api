from django.contrib import admin
from django.urls import path, include
from djoser import urls


urlpatterns = [
    path('', include('main.urls')), 
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
