from django.shortcuts import get_object_or_404, render

from store.models import Car, ProductMedia

def home(request):
    promo_cars = Car.objects.filter(is_on_promo=True)


    context = {'promo_cars':promo_cars}
    return render(request, 'frontend/index.html', context)


def single_car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)
    product_image = ProductMedia.objects.filter(product=car)

    context = {'car': car}
    return render(request, 'frontend/single_car_details.html', context)