# Generated by Django 4.0.1 on 2023-01-11 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Picture',
            new_name='ProductPicture',
        ),
    ]