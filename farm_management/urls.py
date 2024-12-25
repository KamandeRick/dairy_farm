"""Defines URL patterns for farm_management"""

from django.urls import path
from . import views

app_name = 'farm_management'
urlpatterns = [
    #Home page
    # path('', views.index, name='index'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Cow URLs
    path('cows/', views.cow_list, name='cow_list'),
    path('cows/<str:tag_number>/', views.cow_detail, name='cow_detail'),

    # Milk Production URLs
    path('milk-production/', views.milk_production_list, name='milk_production_list'),

    # Veterinary Record URLs
    path('vet-records/', views.vet_record_list, name='vet_record_list'),

    #Create Forms urls
    path('cow/add/', views.add_cow, name='add_cow'),
    path('milk-production/add/', views.add_milk_record, name='add_milk_record'),
    path('vet-records/add/', views.add_vet_record, name='add_vet_record'),

    # Authentication URLs
    path('register/', views.register, name='register'),
]
