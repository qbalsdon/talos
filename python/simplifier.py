#!/usr/bin/env python3
from common import *
from deviceManager import *
import os
import xml.etree.cElementTree as ET


def removeWindowDump(fileReference, device=None):
    adbCommand(["shell", "rm", "/sdcard/"+fileReference], device, output=False)

def fetchDeviceRawData(options = None):
    device = getDevice(options = options)
    OUT_FILE = "window_dump.xml"
    PHONE_FILE="/sdcard/"+OUT_FILE
    removeWindowDump(PHONE_FILE, device)
    adbCommand(["exec-out", "uiautomator", "dump"], device)
    adbCommand(["pull", PHONE_FILE], device, output=False)
    with open(OUT_FILE) as file:
        data = file.read()
    os.remove(OUT_FILE)
    removeWindowDump(PHONE_FILE, device)
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
    return ET.fromstring(data)

def setUp(ui_required = True):
    options = proccessArgs()
    getDevice(options=options)
    if ui_required:
        return options, parseXML(options = options)
    return options
