#! /usr/bin/python3 -OOt

import sys
import subprocess
import inspect

class DrexError(Exception):
    
    def __init__(self,msg,**kwargs):
        self.msg = msg
        try:
            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
        self.args = "{0.__name__} (line {1}): {2}".format(type(self), ln, self.msg),
        sys.exit(self)


class DeviceNotFoundError(DrexError):
    '''Exception Raised when no device found'''
    def __init__(self,**kwargs):
        self.msg = "No devices were found. Try checking if both devices are on the same WiFi network or re-pair if the problem persists"
        super().__init__(self.msg,**kwargs)

files = [str(file) for file in sys.argv[1].split(",")]
_kdeID = subprocess.run(["kdeconnect-cli","-a","--id-only"],capture_output=True).stdout
kdeID = (_kdeID.decode('utf-8')).strip()

if(kdeID):
    share = subprocess.run(["kdeconnect-cli","-d",kdeID,"--share",*files],capture_output=True)
else:
    raise DeviceNotFoundError