#!/usr/bin/env python3
from common import *
from deviceManager import *
import os
import xml.etree.cElementTree as ET


def removeWindowDump(fileReference, device=None):
    adbCommand(["shell", "rm", fileReference], device, output=False)

def fetchWindowDump(device, location, OUT_FILE):
    try:
        adbCommand(["pull", location], device, output=False)
        with open(OUT_FILE) as file:
            data = file.read()
        os.remove(OUT_FILE)
        removeWindowDump(location, device)
        return data
    except FileNotFoundError as e:
        return None

def fetchDeviceRawData(options = None):
    device = getDevice(options = options)
    LOCATIONS=["/storage/emulated/legacy/", "/sdcard/", "/storage/sdcard/"]
    INDEX=0
    OUT_FILE = "window_dump.xml"
    data=None
    while data == None and INDEX < len(LOCATIONS):
        location=f"{LOCATIONS[INDEX]}{OUT_FILE}"
        removeWindowDump(location, device)
        adbCommand(["exec-out", "uiautomator", "dump"], device, output=False)
        data = fetchWindowDump(device, location, OUT_FILE)
        INDEX = INDEX + 1
    return data

def parseXML(data = None, options = None):
    if options != None and "file" in options:
        root = ET.parse(options["file"]).getroot()
        return root
    if options != None and "xml" in options:
        return ET.fromstring(options["xml"])
    if data == None:
        data = fetchDeviceRawData(options)
    # Parse XML with ElementTree
    if data == None:
        raise ValueError("Cannot fetch UI data from device")
    return ET.fromstring(data)

def setUp(ui_required = True):
    options = proccessArgs()
    getDevice(options=options)
    if ui_required:
        return options, parseXML(options = options)
    return options
