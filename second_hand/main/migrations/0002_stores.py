# Generated by Django 4.2.1 on 2023-05-20 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_house', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('name_store', models.CharField(max_length=50)),
                ('time_job', models.TextField()),
                ('number_phone', models.IntegerField()),
                ('store_network', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.storenetwork')),
            ],
        ),
    ]
