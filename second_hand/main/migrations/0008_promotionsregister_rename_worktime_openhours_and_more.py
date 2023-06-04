# Generated by Django 4.2.1 on 2023-05-26 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_worktime'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionsRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_name', models.CharField(max_length=50)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name='WorkTime',
            new_name='OpenHours',
        ),
        migrations.AlterField(
            model_name='openhours',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.stores'),
        ),
        migrations.CreateModel(
            name='PromotionDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField()),
                ('monday', models.IntegerField()),
                ('tuesday', models.IntegerField()),
                ('wednesday', models.IntegerField()),
                ('thursday', models.IntegerField()),
                ('friday', models.IntegerField()),
                ('saturday', models.IntegerField()),
                ('sunday', models.IntegerField()),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.stores')),
            ],
        ),
    ]
