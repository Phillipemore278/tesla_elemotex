from django.db import models
from store.models import Car

class Order(models.Model):
    car =  models.ForeignKey(Car, related_name='order', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    City = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=500)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
