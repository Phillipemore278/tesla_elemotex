from django import forms
from django.core.exceptions import ValidationError
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name:
            existing = Category.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("This category already exists under the selected parent.")
