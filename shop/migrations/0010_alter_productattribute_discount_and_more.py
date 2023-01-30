# Generated by Django 4.0.1 on 2023-01-17 16:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_productattribute_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
