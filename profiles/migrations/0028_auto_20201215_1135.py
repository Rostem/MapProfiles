# Generated by Django 3.1.1 on 2020-12-15 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_auto_20201215_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date_meas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.date_meas'),
        ),
        migrations.AlterField(
            model_name='data',
            name='machine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.machine'),
        ),
    ]
