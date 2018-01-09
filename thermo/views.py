# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from getenv import env
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route
import requests
import subprocess

from datetime import date

from pyHS100 import SmartPlug

from thermo.helpers.helpers import *
from thermo.serializers import *
from thermo.models import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SetupView(generics.ListCreateAPIView):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer

    def perform_create(self, serializer):
        serializer.save()

class SetupDetailView(viewsets.ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer
    lookup_field="name"

    @detail_route(methods=['put'])
    def update(self, request, name=None):
        setup = self.get_object()
        serializer = SetupSerializer(setup, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'setup set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomsView(generics.ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer
    def perform_create(self, serializer):
        serializer.save()

    def list(request, *args, **kwargs):
        rooms = []
        for room in Rooms.objects.all():
            plugs_o = Plugs.objects.all().filter(room_id=room.id)
            plugs = []
            sensors = []
            for plug in plugs_o:
                plugs.append({"id":plug.id, 'ip':plug.ip, "name":plug.name, "state":plug.state})

            sensor_o = Sensors.objects.all().filter(room_id=room.id)
            for sensor in sensor_o:
                if env("DEBUG") == True:
                    data = {"Temperature": "21", "Humidity": "56"}
                else:
                    data = requests.get('http://' + sensor.ip + '/data').json()

                sensors.append({'id': sensor.id, 'name': sensor.name, 'ip': sensor.ip ,'temperature': data['Temperature'], 'humidity': data['Humidity']})
            rooms.append({'id': room.id, 'name': room.name, 'plugs': plugs, 'sensors':sensors})
        return Response(rooms)


class RoomsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer

class PlugsView(generics.ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Plugs.objects.all()
    serializer_class = PlugsSerializer

    def perform_create(self, serializer):
        serializer.save()

class PlugsDetailView(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Plugs.objects.all()
    serializer_class = PlugsSerializer

    @detail_route(methods=['put'])
    def update(self, request, pk=None):
        plug = self.get_object()

        serializer = PlugsSerializer(plug, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                smplug = SmartPlug(request.data['ip'])
                if(request.data['state'] == '1' or request.data['state'] == True):
                    print("test")
                    smplug.turn_on()
                else:
                    print("test2")
                    smplug.turn_off()
                print(serializer.save())
            except:
                return Response({'error': 'Une erreur s\'est produite'})
            return Response({'status': 'state set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorsView(generics.ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(request, *args, **kwargs):
        sensors = []
        for sensor in Sensors.objects.all():
            if env("DEBUG") == True:
                data = {"Temperature": "21", "Humidity": "56"}
            else:
                data = requests.get('http://' + sensor.ip + '/data').json()

            sensors.append({'id':sensor.id, 'name': sensor.name, 'temperature':data['Temperature'], 'humidity':data['Humidity']})
        return Response(sensors)

class SensorsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer

class LogsSensorsView(generics.ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LogsSensors.objects.all()
    serializer_class = LogsSensorsSerializer

    def perform_create(self, serializer):
        serializer.save()

class LogsSensorsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LogsSensors.objects.all()
    serializer_class = LogsSensorsSerializer

class LogsPlugsView(generics.ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LogsPlugs.objects.all()
    serializer_class = LogsPlugsSerializer

    def perform_create(self, serializer):
        serializer.save()

class LogsPlugsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LogsPlugs.objects.all()
    serializer_class = LogsPlugsSerializer

class CheckPresenceView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        p = subprocess.Popen(
            "ping -c1 -W1  iphone-de-sebastien.local | grep -o -E '[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}'",
            stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        output = output.replace("\n", "")
        if output:

            return Response(output)
        else:
            return Response(err)

class CheckDataView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        sensors = {}
        plugs = {}
        response = {}
        response['sensors'] = {}
        for sensor in Sensors.objects.all():
            if env("DEBUG") == True:
                sensors[sensor.name] = {"Temperature": "21", "Humidity": "56"}
            else:
                sensors[sensor.name] = requests.get('http://' + sensor.ip + '/data').json()

            logsSensors = LogsSensors()
            logsSensors.temperature = sensors[sensor.name].get('Temperature')
            logsSensors.humidity = sensors[sensor.name].get('Humidity')
            logsSensors.sensor = sensor
            logsSensors.save()

            logsPlugs = LogsPlugs()
            plugs = Plugs.objects.all().filter(room_id=sensor.room.id)

            BoolInterval = False

            for ti in TimeInterval.objects.all().filter(room_id=sensor.room.id):

                if(isInTimeInterval(ti.startingTime, ti.endingTime)):
                    BoolInterval = True

            print("BoolInterval : "+str(BoolInterval))
            #BoolPlugForced = None
            #for plug in plugs:
            #    if (plug.force == 2):
            #        BoolPlugForced = True
            #    elif (plug.force == 1):
            #        BoolPlugForced = False

            #condition = isSetupTrue("ForceOn") or (isSetupTrue("ForceStop") != True and BoolInterval) and (
            #(date.today().isoweekday() != 6 and date.today().isoweekday() != 7) or isPresent(
            #    'iphone-de-sebastien.local'))

            presenceBool = sensors[sensor.name].get('Presence')
            condition =  (isSetupTrue("ForceStop") != True and presenceBool and BoolInterval == False) or (
                    ((not presenceBool) or BoolInterval) and int(sensors[sensor.name]['Temperature']) < int(Setup.objects.get(name__iexact="MinTemperature").value))

            print("condition1: " + str((isSetupTrue("ForceStop") != True and presenceBool and BoolInterval == False)))
            print("__")
            print("condition2 : " + str(((not presenceBool) or BoolInterval) and int(sensors[sensor.name]['Temperature']) < int(Setup.objects.get(name__iexact="MinTemperature").value)))


            if  condition:
                if presenceBool and (BoolInterval == False):
                    askedTemperature = Setup.objects.get(name__iexact="Temperature").value
                else:
                    askedTemperature = Setup.objects.get(name__iexact="MinTemperature").value

                print(askedTemperature)
                print(sensors[sensor.name]['Temperature'])
                if  int(sensors[sensor.name]['Temperature']) < int(askedTemperature) + 1:
                    response['success'] = True
                    response['sensors'][sensor.name] = {'state': "on"}
                    logsPlugs.value = 1
                    for plug in plugs:
                        if(condition == True):
                            print("ON " + plug.ip)
                            plug.state = True
                            smplug = SmartPlug(plug.ip)
                            smplug.turn_on()
                elif int(sensors[sensor.name]['Temperature']) >= int(askedTemperature) - 1:
                    response['success'] = True
                    response['sensors'][sensor.name] = {'state': "off"}
                    logsPlugs.value = 0
                    for plug in plugs:
                        print("Off " + plug.ip)
                        plug.state = False
                        smplug = SmartPlug(plug.ip)
                        smplug.turn_off()
                else:
                    logsPlugs.value = 0
            else:
                logsPlugs.value = 0
                for plug in plugs:
                    smplug = SmartPlug(plug.ip)
                    plug.state = False
                    smplug.turn_off()

            logsPlugs.save()
            plug.save()
        return JsonResponse(response)
