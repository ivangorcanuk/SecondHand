# Generated by Django 4.2.1 on 2023-07-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_area_stores_address_remove_stores_floor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotiondays',
            name='promotion_days',
        ),
        migrations.RemoveField(
            model_name='promotiondays',
            name='week_number',
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='friday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='monday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='saturday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='sunday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='thursday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='tuesday',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='promotiondays',
            name='wednesday',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
