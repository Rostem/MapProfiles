# Generated by Django 3.1.3 on 2020-12-01 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20201130_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='pattern1',
        ),
        migrations.RemoveField(
            model_name='data',
            name='pattern2',
        ),
    ]
