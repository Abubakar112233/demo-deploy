# Generated by Django 4.0.1 on 2023-02-14 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_useraddressbook_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressbook',
            name='postal_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='town_or_city',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
