# Generated by Django 5.2.1 on 2025-05-18 15:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_productmedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmedia',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
    ]
