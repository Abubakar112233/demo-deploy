# Generated by Django 4.0.1 on 2023-02-01 20:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_product_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]