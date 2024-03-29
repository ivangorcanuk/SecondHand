# Generated by Django 4.2.1 on 2023-05-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_stores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stores',
            name='street_house',
        ),
        migrations.AddField(
            model_name='stores',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='stores',
            name='floor',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='stores',
            name='house',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='stores',
            name='street',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='stores',
            name='time_job',
            field=models.TimeField(),
        ),
    ]
