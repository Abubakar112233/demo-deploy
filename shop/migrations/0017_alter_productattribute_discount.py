# Generated by Django 4.0.1 on 2023-02-05 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_productattribute_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='discount',
            field=models.IntegerField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]
