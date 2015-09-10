#!/usr/bin/env python
# encoding=utf8

from __future__ import (absolute_import, division, print_function, unicode_literals)

"""A utility to upload new firmware to a RobertSonics WavTrigger """

__version__ = '0.1.0'
__author__ = 'Eberhard Fahle'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Eberhard Fahle'

import sys
import os
import time
from serial import Serial,PARITY_EVEN
import argparse

#Hack for making the code work with python 2 and 3
try:
    #if we are on python 2 use raw_input for user confirmation
    input = raw_input
except NameError:
    pass

class IntelHexFile(object):
    """Wraps the data of a firmware file in IntelHexFormat.
    The class reads the file, tests if the checksums match and 
    creates a list of address,data tuples that can be directly uploaded to
    a WavTrigger.

    Note: this only works for a file containing WavTrigger firmware. 
    The class does NOT implement a full IntelHexFile parser.
    """
    def __init__(self,filename): 
        """Loads the firmware file and parses it into 
        a list of bytearrays"""
        #the firmware data to be uploaded to the WavTrigger
        self._firmware=[]
        #test if we have a valid filename for the firmware argument
        self._fn=self._checkFile(filename)
        with open(self._fn,'r') as f:
            self._content=list(f)
        #test the checksums of each line and create the data-records
        self._processFile()

    def getFirmware(self):
        """Returns a copy of the data in the HexFile as list of 
        bytearray elements, ready for sending to the WavTrigger
        """
        return self._firmware[:]

    def getFilename(self):
        """Gets the original path from which the firmware was loaded.""" 
        return self._fn

    def _checkFile(self,filename):
        fn=os.path.abspath(filename)
        if not os.path.isfile(fn):
            raise ValueError("File : '"+fn+"' does not exist or is not a file!")
        if not os.access(fn,os.R_OK):
            raise ValueError("File : '"+fn+"' cannot be opened for reading!")
        return fn

    def _processFile(self):
        if len(self._content)==0:
            raise ValueError('File is empty')
        lineNumber=0
        for l in self._content: 
            lineNumber+=1
            if not l.startswith(':'):
                err='Invalid prefix on line : '+str(lineNumber)
                raise ValueError(err)
            #slice the leading colon and the line break
            l=l[1:-1]
            recLength=int(l[0:2],16)
            recAddress=int(l[2:6],16)
            recType=int(l[6:8],16)
            recCheckSum=int(l[-2:],16)
            #Test the checksum of the hexfile entry 
            checkSum=0x00
            for i in range(0,len(l)-1,2):
                checkSum=checkSum+int(l[i:i+2],16)
            checkSum=checkSum & 0xFF
            if checkSum:
                raise ValueError("Invalid checksum:"+str(checkSum)+" on Line:"+str(lineNumber))

            #Now process the data to be uploaded 
            #We can safely ignore all lines that are not Data Records
            if recType==0x00:
                address=bytearray([0x08,0x00,(recAddress>>8)&0xFF,recAddress&0xFF])
                addressCheckSum=0
                for a in address:
                    addressCheckSum=addressCheckSum^a
                address.append(addressCheckSum)
                data=bytearray()
                #The first byte contains the number of bytes-1 to be written
                data.append(recLength-1)
                for i in range(0,2*recLength,2):
                    data.append(int(l[i+8:i+10],16))
                dataCheckSum=0
                for d in data:
                    dataCheckSum=dataCheckSum^d
                data.append(dataCheckSum)
                #print(binascii.hexlify(data))
                #save the data in a tuple with format (address,data)
                self._firmware.append((address,data))

class CmdParser(object):
    """Wraps the parser for commandline arguments"""
    def __init__(self):
        self._parser=argparse.ArgumentParser(description='Firmware update utility for the WavTrigger',
                prog='wt-flasher')
        self._parser.add_argument('-d','--DoNotAsk',
                action='store_false',  
                help='Run upload without explicit user confirmation')
        self._parser.add_argument('-f','--firmware',
                action='store',
                default='',
                required=True,
                help='Path to the Firmware update')
        self._parser.add_argument('-p','--port',
                action='store',
                default='',
                required=True,
                help='Serial port where the WavTrigger is listening')

    def parse(self,userArgs):
        return self._parser.parse_args(userArgs).__dict__

class Uploader(object):
    """Connects to the WavTrigger and uploads the firmware"""
    _serialSpeed=57600
    _serialParity=PARITY_EVEN

    _DOWNSTREAM_OK='\x79'

    _UPSTREAM_CONTACT_RETRIES=50
    _UPSTREAM_CONTACT=bytearray([0x7f])

    _UPSTREAM_VERSION=bytearray([0x00,0xFF])

    _UPSTREAM_EXTENDED_ERASE=bytearray([0x44,0xBB])
    _UPSTREAM_EXTENDED_ERASE_START=bytearray([0xFF,0xFF,0x00])

    _UPSTREAM_WRITE_MEMORY=bytearray([0x31,0xCE])

    def __init__(self,port,hexfile):
        self.serial=Serial(baudrate=Uploader._serialSpeed,
                parity=Uploader._serialParity)
        self.serial.port=port
        self.dataFile=hexfile

    def run(self):
        """Upload the data to the WavTrigger"""
        try:
            self.serial.open()
            if self._contact():
                print("Found WavTrigger on port '"+self.serial.port+"'")
            else:
                raise ValueError("WavTrigger on port '"+self.serial.port+"' does not respond")
            print("Checking version ...",end=" ")
            sys.stdout.flush()
            if self._version():
                print("OK")
            else:
                raise ValueError("WavTrigger on port '"+self.serial.port+"' does not report valid version data")
            print("Erase current firmware on the WavTrigger ...",end=" ")
            sys.stdout.flush()
            if self._erase():
                print("OK")
            else:                
                raise ValueError("WavTrigger on port '"+self.serial.port+"' erase failed")
            print("Upload new Firmware '"+self.dataFile.getFilename()+"'", end=" ... ")
            sys.stdout.flush()
            if self._pgm():
                print("OK")
            else:    
                raise ValueError("WavTrigger on port '"+self.serial.port+"' upload failed")
        except ValueError as err:
            print(err)
        finally:            
            self.serial.close()

    def _contact(self):
        """Send a contact request to the WavTrigger until the WT
        answers with the _DOWNSTREAM_OK token or the contact request times out
        """
        self.serial.timeout=0.225
        for r in range(Uploader._UPSTREAM_CONTACT_RETRIES):
            self.serial.write(Uploader._UPSTREAM_CONTACT)
            if self._checkDownstreamOK():
                return True
        return False

    def _version(self):
        """Send the version command to the WavTrigger and read the response.
        """
        self.serial.timeout=5.0
        self.serial.write(Uploader._UPSTREAM_VERSION)
        if self._checkDownstreamOK():
            result=self.serial.read(1)
            if len(result):
                version_length=ord(result[0])
                #print(version_length)
                if version_length>64 :
                    #The original code marks this somehow as an error 
                    return False
                version=self.serial.read(version_length)
                if len(version)==version_length:
                    #No information in available on the exact meaning of the
                    #version string. We assume that the request was sucessful
                    #if the WavTrigger returns the correct lenth
                    return True
        #The WavTrigger does not return a valid version string               
        return False

    def _erase(self):
        """Erase old firmware from the WavTrigger
        """
        self.serial.flushInput()
        self.serial.timeout=0.5
        self.serial.write(Uploader._UPSTREAM_EXTENDED_ERASE)
        if self._checkDownstreamOK(timeout=0.5):
            self.serial.write(Uploader._UPSTREAM_EXTENDED_ERASE_START)
            self.serial.flushInput()
            if self._checkDownstreamOK(timeout=30.0):
                return True
        return False

    def _pgm(self):
        """Upload new firmware to the WavTrigger
        """
        firmware=self.dataFile.getFirmware()
        uploaded=0
        for entry in firmware:
            self.serial.timeout=5.0
            self.serial.flushInput()
            self.serial.write(Uploader._UPSTREAM_WRITE_MEMORY)
            if not self._checkDownstreamOK():
                return False
            self.serial.flushInput()
            self.serial.write(entry[0])
            if not self._checkDownstreamOK():
                return False
            self.serial.flushInput()
            self.serial.write(entry[1])
            if not self._checkDownstreamOK():
                return False
        #All data written successfully 
        return True

    def _checkDownstreamOK(self,timeout=None):
        """Test if the WavTrigger acknowledges a positve result for the 
        last operation
        """
        if timeout is not None: 
            self.serial.timeout=timeout
        result=self.serial.read(1)
        if len(result)==1 and result==Uploader._DOWNSTREAM_OK:
            return True
        return False


def upload():
    """Entrypoint for the application"""
    cmdP=CmdParser()
    args=cmdP.parse(sys.argv[1:])
    firmware=IntelHexFile(args['firmware'])
    uploader=Uploader(port=args['port'],hexfile=firmware)
    if args['DoNotAsk']==True:
        print('This will erase and overwrite the current firmware of the WavTrigger!')
        result=input("Type 'yes' and hit <return> to proceed : ")
        if result.lower()!='yes':
            print("Upload aborted")
            exit()
    uploader.run()
    exit()

if __name__ == '__main__':
    upload()


