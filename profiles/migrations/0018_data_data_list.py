# Generated by Django 3.1.1 on 2020-12-14 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_auto_20201213_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='data_list',
            field=models.TextField(default=None, help_text='list of selected files'),
        ),
    ]