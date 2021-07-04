#!/usr/bin/env python3
from common import *
from deviceManager import *
from fetchUI import *

def setUp(ui_required = True):
    options = proccessArgs()
    getDevice(options=options)
    if ui_required:
        return options, parseXML(options = options)
    return options
