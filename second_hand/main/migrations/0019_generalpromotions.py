# Generated by Django 4.2.1 on 2023-09-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_stores_open_hours_alter_stores_promotion_days_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralPromotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('decoding', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
