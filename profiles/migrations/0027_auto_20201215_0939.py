# Generated by Django 3.1.1 on 2020-12-15 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_auto_20201215_0825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='default_config_path',
            new_name='default_data_path',
        ),
    ]