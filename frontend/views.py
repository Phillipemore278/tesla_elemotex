from django.shortcuts import get_object_or_404, render

from store.models import Category, Car, ProductMedia

def home(request):
    promo_cars = Car.objects.filter(is_on_promo=True)


    context = {'promo_cars':promo_cars}
    return render(request, 'frontend/index.html', context)


def single_car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)
    
    context = {'car': car}
    return render(request, 'frontend/single_car_details.html', context)

def inventory(request):
    category_list = Category.objects.all()

    # Get filter values
    selected_slug = request.GET.getlist('category', 'all')

    car_list = Car.objects.all()

     # Optional: Filter further if user selected specific categories
    if selected_slug and 'all' not in selected_slug:
        car_list = Car.objects.filter(category__slug__in=selected_slug)


    context = {'car_list':car_list, 'selected_slug':selected_slug,
            'category_list':category_list}
    return render(request, 'frontend/inventory.html', context)