from django.contrib.auth.models import User, Group
from rest_framework import serializers

from thermo.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class SetupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Setup
        fields = ('id', 'name', 'value')

class RoomsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rooms
        fields = ('id', 'name')

class PlugsSerializer(serializers.HyperlinkedModelSerializer):
    #room = RoomsSerializer(required=False)
    room = serializers.HyperlinkedRelatedField(
        queryset=Rooms.objects.all(),
        view_name='room-detail'
    )
    class Meta:
        model = Plugs
        fields = ('name', 'ip', 'state', 'room', 'force')

class SensorsSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        queryset=Rooms.objects.all(),
        view_name='room-detail'
    )
    class Meta:
        model = Sensors
        fields = ('name', 'ip', 'room')

class LogsSensorsSerializer(serializers.HyperlinkedModelSerializer):
    sensor = SensorsSerializer()
    class Meta:
        model = LogsSensors
        fields = ('date', 'temperature', 'humidity', "sensor")

class LogsPlugsSerializer(serializers.HyperlinkedModelSerializer):
    plug = PlugsSerializer()
    class Meta:
        model = LogsPlugs
        fields = ('date', 'value', "plug")
