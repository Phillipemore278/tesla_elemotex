import secrets
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse

def generate_unique_suffix():
    return f"{secrets.token_hex(2)}{str(uuid.uuid4())[:4]}"


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        # Check if a category with the same name and same parent already exists
        existing = Category.objects.filter(name__iexact=self.name)
        if self.pk:
            existing = existing.exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError("A category with this name already exists.")
    
    def save(self, *args, **kwargs):
        self.clean()  # call clean to validate
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:category_detail", kwargs={"slug": self.slug})


class Car(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='cars')
    title = models.CharField(max_length=255)
    description = models.TextField()
    car_range = models.CharField(max_length=50)
    top_speed = models.CharField(max_length=50)
    peak_power = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    miles = models.CharField(max_length=50)
    is_on_promo = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    year = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    doors = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            while Car.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{generate_unique_suffix()}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def featured_image(self):
        return self.media.filter(is_featured=True).first()


class ProductMedia(models.Model):
    product = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='product_media/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Media for {self.product.title}"
    
    def save(self, *args, **kwargs):
        # Check if any media for this product is already featured
        existing_featured = ProductMedia.objects.filter(product=self.product, is_featured=True)

        # If none is featured and this one isn't explicitly marked, auto-feature it
        if not existing_featured.exists() and not self.is_featured:
            self.is_featured = True

        # If this one is featured, unset others
        if self.is_featured:
            ProductMedia.objects.filter(product=self.product, is_featured=True).exclude(pk=self.pk).update(is_featured=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if this was the featured image
        was_featured = self.is_featured
        product = self.product
        super().delete(*args, **kwargs)

        # If it was featured, promote another media
        if was_featured:
            next_media = ProductMedia.objects.filter(product=product).first()
            if next_media:
                next_media.is_featured = True
                next_media.save()
