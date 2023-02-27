# Generated by Django 4.1.5 on 2023-02-22 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_cartorder_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name_plural': 'Banners'},
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='cartorder',
            options={'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': 'Order Items'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': 'Colors'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name_plural': 'Sizes'},
        ),
    ]
