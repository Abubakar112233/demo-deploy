# Generated by Django 4.0.1 on 2023-02-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_productattribute_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='banner_type',
            field=models.CharField(choices=[('productdiscount', 'Product Discount'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='process', max_length=150),
        ),
    ]
