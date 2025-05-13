from django.contrib import admin
from .models import Category, Car, ProductMedia
from .forms import CategoryForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['name', 'slug']


class ProductMediaInline(admin.TabularInline):  # or StackedInline for image previews
    model = ProductMedia
    extra = 1
    fields = ['image', 'alt_text', 'is_featured']
    readonly_fields = []

@admin.register(Car)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_on_promo', 'category', 'slug']
    inlines = [ProductMediaInline]


# @admin.register(ProductMedia)
# class ProductMediaAdmin(admin.ModelAdmin):
#     list_display = ['product', 'image', 'is_featured']
