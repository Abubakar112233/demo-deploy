# Generated by Django 4.0.1 on 2023-01-11 21:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productattribute_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='discount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
