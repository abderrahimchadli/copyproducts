# Generated by Django 3.2.15 on 2022-10-24 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_auto_20221024_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='authappshopuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authappshopuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
