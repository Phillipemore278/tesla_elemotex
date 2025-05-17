from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Car  

def category_detail(request, slug):
    # Get the current category
    category = get_object_or_404(Category, slug=slug)

    # Get filter values
    selected_slug = request.GET.getlist('category', 'all')

    print(selected_slug)

    # If selected_slug is a list and not empty, use the first item. Otherwise, use 'all'
    if selected_slug:
        selected_slug = selected_slug[0]  # Extract the first item from the list
    else:
        selected_slug = 'all'
    # Get products in current category
    car_list = category.cars.all()  # using related_name='cars'

    print(selected_slug)
     # Optional: Filter further if user selected specific categories
    if  selected_slug != 'all':
        car_list = Car.objects.filter(category__slug__in=selected_slug)
        print('this is selected slug', selected_slug)
        print(car_list)
        print()
    else:
        print('not in')
        car_list = Car.objects.filter(category=category)

    category_list = Category.objects.all()


    return render(request, 'store/category_detail.html', {
        'category': category,
        'car_list': car_list,
        'category_list': category_list,
        'selected_slug': selected_slug,
    })