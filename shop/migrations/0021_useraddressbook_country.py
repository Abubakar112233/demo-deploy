# Generated by Django 4.0.1 on 2023-02-14 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressbook',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.countries'),
        ),
    ]
