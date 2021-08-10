#!/usr/bin/env python3

import os
import re
import subprocess
from functools import partial
from common import *

def process_device(data):
    if "\t" in data:
        ndata = data.split("\t")
        return {"Name": ndata[0], "Status": ndata[1]}
    return None

def getConnectedDevices():
    result = adbCommand(["devices"])
    devices = []
    for line in result.splitlines():
        device = process_device(line)
        if not device == None:
            devices.append(device)
    return devices

def statusFilter(deviceMap):
    if deviceMap.get("Status") == "device":
        return True
    else:
        return False

def deviceFilter(deviceMap):
    if "emulator" in deviceMap.get("Name"):
        return False
    else:
        return True

def preferredFilter(deviceMap, preferred = None):
    if preferred == None:
        return False

    if preferred == deviceMap.get("Name") and deviceMap.get("Status") == "device":
        return True
    else:
        return False

def getDevice(deviceList = None, options = None):
    if options == None:
        options = proccessArgs()

    if options.get("device") != None:
        return options.get("device")

    if options.get("preferredDevice") == None:
        options["preferredDevice"] = os.environ['ADB_DEFAULT'] #TODO: dependency injection!

    if deviceList == None:
        deviceList = getConnectedDevices()

    if len(deviceList) == 0:
        print("No devices/emulators found - empty connection list")
        return None

    connectedDevices = list(filter(statusFilter, deviceList))

    if len(connectedDevices) == 0:
        print("No authorised devices/emulators found")
        return None

    physicalConnectedDevices = list(filter(deviceFilter, connectedDevices))
    if len(physicalConnectedDevices) > 0:
        preferredDevice = options.get("preferredDevice")
        partialFilter = partial(preferredFilter, preferred=preferredDevice)
        preference = list(filter(partialFilter, physicalConnectedDevices))
        if len(preference) == 1:
            options["device"] = preference[0].get('Name')
            return options.get("device")
        elif preferredDevice != None:
            raise ValueError("!! Prefered device [" + preferredDevice + "] not connected !!")
            return None

        options["device"] = physicalConnectedDevices[0].get('Name')
        return options.get("device")

    options["device"] = connectedDevices[0].get('Name')
    return options.get("device")

def getScreenSize(rawData = None, options = None):
    if rawData == None:
        rawData = adbCommand(["shell", "wm", "size"], getDevice(options = options))
    sizeArr = re.findall(r"\d+", rawData)
    if len(sizeArr) != 2:
        return None
    return {"width": int(sizeArr[0]), "height": int(sizeArr[1])}

if __name__ == "__main__":
    print(getConnectedDevices())
    print("----------")
    print(getDevice())
    print("----------")
    print(getScreenSize())
