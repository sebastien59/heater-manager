from thermo.models import Setup, Plugs
from datetime import datetime, time

def isSetupTrue(param):
    return (Setup.objects.get(name__iexact=param).value == "1")

def isPlugForced(plug_id):
    return Plugs.objects.get(pk=plug_id).force

def isInTimeInterval(datetime1= None, datetime2=None):
    current_time = datetime.now().time()
    return datetime1 <= current_time <= datetime2