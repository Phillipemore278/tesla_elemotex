# Generated by Django 5.2.1 on 2025-05-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='City',
            new_name='city',
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='1234567890', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='zip_code',
            field=models.CharField(max_length=50),
        ),
    ]
