# Generated by Django 4.2.1 on 2023-05-31 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_stores_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stores',
            name='slug',
        ),
    ]
