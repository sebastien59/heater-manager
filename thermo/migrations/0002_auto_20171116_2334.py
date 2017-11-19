# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thermo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('startingTime', models.DateTimeField()),
                ('endingTime', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='plugs',
            name='force',
            field=models.IntegerField(default=0),
        ),
    ]
