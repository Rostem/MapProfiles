# Generated by Django 3.1.1 on 2020-12-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0024_auto_20201215_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='default_config_path',
            field=models.CharField(blank=True, default=None, max_length=200),
        ),
    ]