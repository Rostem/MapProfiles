# Generated by Django 3.1.3 on 2020-11-23 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20201122_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='baseline_path',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_path',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
