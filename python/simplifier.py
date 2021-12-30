#!/usr/bin/env python3
from common import *
from deviceManager import *
import os
import xml.etree.cElementTree as ET


def removeWindowDump(fileReference, device=None):
    adbCommand(["shell", "rm", "/sdcard/"+fileReference], device, output=False)

def fetchWindowDump(device, location, OUT_FILE):
    try:
        removeWindowDump(location, device)
        adbCommand(["exec-out", "uiautomator", "dump"], device)
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
    OUT_FILE = "window_dump.xml"
    PHONE_FILE="/sdcard/"+OUT_FILE
    ALT_PHONE_FILE="/storage/sdcard/"+OUT_FILE

    data = fetchWindowDump(device, PHONE_FILE, OUT_FILE)
    if data == None:
        print("\n!!Failed at " + PHONE_FILE + " attempting " + ALT_PHONE_FILE + " [/storage/sdcard/window_dump.xml]!!\n")
        fetchWindowDump(device, ALT_PHONE_FILE, OUT_FILE)
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
