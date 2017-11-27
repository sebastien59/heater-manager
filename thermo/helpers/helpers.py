from thermo.models import Setup, Plugs
from datetime import datetime, time
import subprocess

def isSetupTrue(param):
    return (Setup.objects.get(name__iexact=param).value == "1")

def isPlugForced(plug_id):
    return Plugs.objects.get(pk=plug_id).force

def isInTimeInterval(datetime1= None, datetime2=None):
    current_time = datetime.now().time()
    return datetime1 <= current_time <= datetime2

def isPresent(deviceName):
        p = subprocess.Popen(
            "ping -c1 -W1  "+deviceName+" | grep -o -E '[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}'",
            stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        output = output.replace("\n", "")
        if output:
            return True
        else:
            return err