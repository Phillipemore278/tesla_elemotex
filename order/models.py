from django.db import models

from store.models import Car, generate_unique_suffix

class Order(models.Model):
    car =  models.ForeignKey(Car, related_name='order', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    order_key = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.order_key:
            self.order_key = generate_unique_suffix()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
