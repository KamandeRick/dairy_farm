"""Defines URL patterns for farm_management"""

from django.urls import path
from . import views

'''app_name = 'farm_management'
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
]'''


app_name = 'farm_management'
urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Cow URLs
    path('cows/', views.CowListView.as_view(), name='cow_list'),
    path('cows/<str:tag_number>/', views.CowDetailView.as_view(), name='cow_detail'),
    path('cows/add/', views.CowCreateView.as_view(), name='add_cow'),
    path('cows/<str:pk>/update/', views.CowUpdateView.as_view(), name='update_cow'),
    path('cows/<str:pk>/delete/', views.CowDeleteView.as_view(), name='delete_cow'),

    # Milk Production URLs
    path('milk-production/', views.MilkProductionListView.as_view(), name='milk_production_list'),
    path('milk-production/add/', views.MilkProductionCreateView.as_view(), name='add_milk_record'),
    path('milk-production/<int:pk>/update/', views.MilkProductionUpdateView.as_view(), name='update_milk_record'),
    path('milk-production/<int:pk>/delete/', views.MilkProductionDeleteView.as_view(), name='delete_milk_record'),

    # Veterinary Record URLs
    path('vet-records/', views.VetRecordListView.as_view(), name='vet_record_list'),
    path('vet-records/add/', views.VetRecordCreateView.as_view(), name='add_vet_record'),
    path('vet-records/<int:pk>/update/', views.VetRecordUpdateView.as_view(), name='update_vet_record'),
    path('vet-records/<int:pk>/delete/', views.VetRecordDeleteView.as_view(), name='delete_vet_record'),

    # Farm URLs
    path('farm/update/', views.FarmUpdateView.as_view(), name='update_farm'),

    # Authentication URLs
    path('register/', views.register, name='register'),
]
