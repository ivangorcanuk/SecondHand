# Generated by Django 4.2.1 on 2023-10-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_stores_latitude_stores_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stores',
            name='number_phone',
            field=models.CharField(max_length=17),
        ),
    ]