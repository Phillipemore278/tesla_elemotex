from django.urls import path

from . import views
app_name = 'order'

urlpatterns = [
    path('order/success/<str:order_key>/', views.order_successful, name='order_succesful'),
]