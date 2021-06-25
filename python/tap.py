#!/usr/bin/env python3
from common import *
from deviceManager import *
from fetchUI import *
from midOf import *

tap_usage="""
  tap [-s DEVICE] [-f XML_FILE | -x XML_RESOURCE]
       -e ELEMENT_MATCHER |
       -prop ELEMENT_PROPERTY -v ELEMENT_PROPERT_VALUE
"""

if __name__ == "__main__":
    options = proccessArgs()
    uiRoot = parseXML(options = options)
    mid = midOf(options, uiRoot)
    if mid != None:
        adbCommand(["shell", "input", "tap", str(mid.get("x")), str(mid.get("y"))], device=options.get("device"), output=False)
    else:
        print("Element not found")
