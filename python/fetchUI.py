#!/usr/bin/env python3
from common import *
from deviceManager import *
import os
import xml.etree.cElementTree as ET

def parseXML(data = None, options = None):
    if data == None:
        data = fetchDeviceRawData(options)
    # Parse XML with ElementTree
    root = ET.fromstring(data)

    return root

def fetchDeviceRawData(options = None):
    device = getDevice(options = options)
    adbCommand(["exec-out" "uiautomator", "dump"], device)
    OUT_FILE = "window_dump.xml"
    adbCommand(["pull", "/sdcard/"+OUT_FILE], device, output=False)
    with open(OUT_FILE) as file:
        data = file.read()
    os.remove(OUT_FILE)
    return data

if __name__ == "__main__":
    print(parseXML())
