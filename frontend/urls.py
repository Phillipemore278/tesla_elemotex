from django.urls import path

from . import views
app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('car-details/<slug>/', views.single_car_details, name='single_car_details'),
    path('inventory-list/', views.inventory, name='inventory'),
    path('Promo-Cars/', views.promo_car_list, name='promo_car_list'),
]