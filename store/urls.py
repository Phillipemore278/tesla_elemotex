from django.urls import path

from . import views
app_name = 'store'

urlpatterns = [
    path('model-list/<slug:slug>/', views.category_detail, name='category_detail'),
]