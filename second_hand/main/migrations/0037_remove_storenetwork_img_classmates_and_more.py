# Generated by Django 4.2.1 on 2023-10-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_storenetwork_img_classmates_storenetwork_img_inst_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storenetwork',
            name='img_classmates',
        ),
        migrations.RemoveField(
            model_name='storenetwork',
            name='img_inst',
        ),
        migrations.RemoveField(
            model_name='storenetwork',
            name='img_tik_tok',
        ),
        migrations.RemoveField(
            model_name='storenetwork',
            name='img_vk',
        ),
        migrations.RemoveField(
            model_name='storenetwork',
            name='image',
        ),
        migrations.AddField(
            model_name='storenetwork',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='main.gallery'),
        ),
    ]