#! /usr/bin/python3 -OOt

import os
import sys
import subprocess
import inspect
import logging 
import glob

homeDir = os.environ["HOME"]
baseDir = f"{homeDir}/.local/share/kconnectnemo"
logfile = f"{baseDir}/kconnectnemo.log"
logstate = "exists"
baseDirState = "exists"

#check if the base directory exists or has been somehow damaged/deleted
if not glob.glob(baseDir):
    os.mkdir(baseDir) #creates new base directory, this is not normal and should not happen!
    baseDirState = "created"

try:
    file = open(logfile,"r+")
except:
    file = open(logfile,"a+")
    logstate = "created"    

'''Log messages will be improved in the future.'''
logging.basicConfig(filename=logfile, filemode="a+",format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("\n"+"-"*20+"Log Start"+"-"*20)

if(baseDirState=="created"):
    logging.warning(f"Base directory created at {baseDir}. This is not normal and your files might be damaged/missing.")

if(logstate=="created"):
    logging.info(f"Log file created at {logfile}")

class DrexError(Exception):
    '''Custom exception class by drexfall that implements a custom traceback message'''

    def __init__(self,msg,**kwargs):
        self.msg = msg
        try:
            #check if an error line number exists
            ln = sys.exc_info()[-1].tb_lineno 

        except AttributeError:
             #use the child class as the error line
            ln = inspect.currentframe().f_back.f_lineno

        #output the child message as the error with child class name and line number
        self.args = "{0.__name__} (line {1}): {2}".format(type(self), ln, self.msg), 
        
        #exit the interpreter
        sys.exit(self) 


class DeviceNotFoundError(DrexError):
    '''Exception raised when no device is found'''

    def __init__(self,**kwargs):
        self.msg = "No devices were found. Try checking if both devices are on the same WiFi network or re-pair if the problem persists"
        super().__init__(self.msg,**kwargs)

class NoFileError(DrexError):
    '''Exception raised when no file is given as argument'''

    def __init__(self,**kwargs):
        self.msg = "No files where selected to share. Try selecting one or more files this time"
        super().__init__(self.msg,**kwargs)

try:
    files = [str(file) for file in sys.argv[1].split(",")]

    #catch the result of kdeconnect-cli -a --id-only
    _kdeID = subprocess.run(["kdeconnect-cli","-a","--id-only"],capture_output=True).stdout 

    #convert byte object to string and remove newline and whitespace characters
    kdeID = (_kdeID.decode('utf-8')).strip() 

    try:
        if(kdeID):
            share = subprocess.run(["kdeconnect-cli","-d",kdeID,"--share",*files],capture_output=True)
            logging.info(str(share))
        else:
            logging.error("No device was found connected to KDE Connect. Process was aborted.")
            raise DeviceNotFoundError
    except Exception as e:
        logging.error("Exception occured after checking for device ID",exc_info=True)

except IndexError:
    logging.error("No file name specified. Atleast one file should be given as an argument. Process aborted",exc_info=True)    
    raise NoFileError

except Exception as e:
    logging.error("Exception occured before checking for device ID",exc_info=True)
