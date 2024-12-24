"""Defines URL patterns for farm_management"""

from django.urls import path
from . import views

app_name = 'farm_management'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
]
