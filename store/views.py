from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Car  

def category_detail(request, slug):
    # Get the current category
    category = get_object_or_404(Category, slug=slug)

    car_list = category.cars.all()  

    return render(request, 'store/category_detail.html', {
        'category': category,
        'car_list': car_list,
    })