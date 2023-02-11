# Generated by Django 4.0.1 on 2023-02-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=50)),
                ('currency_short_name', models.CharField(max_length=10)),
                ('currency_symbol', models.CharField(max_length=10)),
                ('currency_price', models.FloatField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]