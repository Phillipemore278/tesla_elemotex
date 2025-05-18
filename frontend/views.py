from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse

from store.models import Category, Car, ProductMedia
from order import forms 

def home(request):
    promo_cars = Car.objects.filter(is_on_promo=True)[:8]


    context = {'promo_cars':promo_cars}
    return render(request, 'frontend/index.html', context)


def single_car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)
    form = forms.OrderForm()  # Do not bind request.POST here
    context = {'car': car, 'form': form}
    return render(request, 'frontend/single_car_details.html', context)


def process_order(request):
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        slug = request.POST.get('car_slug')
        car = get_object_or_404(Car, slug=slug)

        if form.is_valid():
            order = form.save(commit=False)  
            order.car = car                  
            order.save()                     
            # messages.success(request, 'Your order was placed successfully.')
            return redirect('order:order_succesful', order_key=order.order_key)
        else:
            messages.error(request, 'Something went wrong, please try again.')
            return redirect('frontend:single_car_details', slug=slug)
    return redirect('frontend:home')  # fallback


def inventory(request):
    category_list = Category.objects.all()
    selected_slug = request.GET.get('category', 'all')

    # Default: all cars and "All Models" label
    car_list = Car.objects.all()
    selected_category_name = "All Models"

    # Apply category filter if a specific one is selected
    if selected_slug != 'all':
        car_list = car_list.filter(category__slug=selected_slug)
        category = Category.objects.filter(slug=selected_slug).first()
        if category:
            selected_category_name = category.name

    # Pagination
    paginator = Paginator(car_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Smart pagination range (window around current page)
    current = page_obj.number
    total = paginator.num_pages
    start = max(current - 2, 1)
    end = min(current + 2, total)
    custom_page_range = range(start, end + 1)

    context = {
        'car_list': page_obj,
        'page_obj': page_obj,
        'selected_slug': selected_slug,
        'selected_category_name': selected_category_name,
        'category_list': category_list,
        'custom_page_range': custom_page_range,
        'total_pages': total,
    }

    return render(request, 'frontend/inventory.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string

def inventory_ajax(request):
    selected_slug = request.GET.get('category', 'all')
    car_list = Car.objects.all().order_by('-id')
    selected_category_name = "All Models"

    if selected_slug != 'all':
        car_list = car_list.filter(category__slug=selected_slug).order_by('-id')
        category = Category.objects.filter(slug=selected_slug).first()
        if category:
            selected_category_name = category.name

    paginator = Paginator(car_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    current = page_obj.number
    total = paginator.num_pages
    start = max(current - 2, 1)
    end = min(current + 2, total)
    custom_page_range = range(start, end + 1)

    context = {
        'car_list': page_obj,
        'page_obj': page_obj,
        'selected_slug': selected_slug,
        'selected_category_name': selected_category_name,
        'custom_page_range': custom_page_range,
        'total_pages': total,
        'total_count': page_obj.paginator.count,
    }

    html = render_to_string('frontend/partials/car_list.html', context)
    pagination_html = render_to_string('frontend/partials/pagination.html', context)

    return JsonResponse({
        'html': html,
        'pagination_html': pagination_html,
        'total_count': context['total_count'],
        'selected_category_name': context['selected_category_name']
    })


def promo_car_list(request):
    promo_cars = Car.objects.filter(is_on_promo=True)

    # Pagination
    paginator = Paginator(promo_cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promo_cars':page_obj,
        'page_obj': page_obj,
        }
    return render(request, 'frontend/promo_cars.html', context)
