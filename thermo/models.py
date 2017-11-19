# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Setup(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.name


class Rooms(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class TimeInterval(models.Model):
    name = models.CharField(max_length=20)
    startingTime = models.TimeField()
    endingTime = models.TimeField()
    room = models.ForeignKey('Rooms', null=True)

    def __str__(self):
        return self.name

class Plugs(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=15)
    state = models.BooleanField(default=0)
    room = models.ForeignKey('Rooms', null=True)
    force = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Sensors(models.Model):
    name = models.CharField(max_length=20)
    ip = models.CharField(max_length=15)
    room = models.ForeignKey('Rooms', null=True)

    def __str__(self):
        return self.name

class LogsSensors(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    sensor = models.ForeignKey('Sensors', null=True)

    def __str__(self):
        return self.id

class LogsPlugs(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()
    plug = models.ForeignKey('Plugs', null=True)

    def __str__(self):
        return self.id