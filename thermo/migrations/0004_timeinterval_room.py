# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thermo', '0003_auto_20171116_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeinterval',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='thermo.Rooms'),
        ),
    ]
