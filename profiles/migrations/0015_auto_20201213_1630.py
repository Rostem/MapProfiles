# Generated by Django 3.1.3 on 2020-12-14 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_data_default_config_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='config_path',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]