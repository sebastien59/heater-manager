# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-02 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogsPlugs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LogsSensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.IntegerField()),
                ('humidity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Plugs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=15)),
                ('state', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('ip', models.CharField(max_length=15)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='thermo.Rooms')),
            ],
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='plugs',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='thermo.Rooms'),
        ),
        migrations.AddField(
            model_name='logssensors',
            name='sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='thermo.Sensors'),
        ),
        migrations.AddField(
            model_name='logsplugs',
            name='plug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='thermo.Plugs'),
        ),
    ]
