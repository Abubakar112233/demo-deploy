# Generated by Django 4.0.1 on 2023-02-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_remove_banner_banner_type_banner_discount_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.TextField()),
                ('delivery_price', models.FloatField(default=25.0)),
            ],
        ),
    ]