from django import forms
from django.core.exceptions import ValidationError

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'city', 'zip_code', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define placeholders for each field
        placeholders = {
            'full_name': 'Enter your full name',
            'email': 'Enter your email address',
            'city': 'Enter your city',
            'zip_code': 'Enter your zip code',
            'phone_number': 'Enter your phone number',
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, '')
            })