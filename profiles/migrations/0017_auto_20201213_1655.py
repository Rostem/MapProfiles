# Generated by Django 3.1.3 on 2020-12-14 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20201213_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='default_config_path',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
