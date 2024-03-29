# Generated by Django 4.2.1 on 2023-06-27 18:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_openhours_store_remove_promotiondays_friday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openhours',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='saturday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='sunday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='wednesday',
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='week_number',
        ),
        migrations.AddField(
            model_name='openhours',
            name='fri_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='fri_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='mon_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='mon_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='sat_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='sat_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='sun_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='sun_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='thu_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='thu_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='tue_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='tue_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='wed_fn',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='openhours',
            name='wed_st',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
