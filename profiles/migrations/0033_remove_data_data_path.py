# Generated by Django 3.1.3 on 2020-12-17 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0032_auto_20201216_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='data_path',
        ),
    ]