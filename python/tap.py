#!/usr/bin/env python3
from simplifier import setUp
from common import adbCommand
from midOf import midOf

tap_usage="""
  tap [-s DEVICE] [-f XML_FILE | -x XML_RESOURCE]
       -e ELEMENT_MATCHER |
       -prop ELEMENT_PROPERTY -v ELEMENT_PROPERT_VALUE
"""

def tap_element(options, root):
    mid = midOf(options, root)
    if mid != None:
        device = options.get("device")
        # print(f"   --> Tapping [{device}] at [{mid}]")
        adbCommand(["shell", "input", "tap", str(mid.get("x")), str(mid.get("y"))], device=device, output=False)
    else:
        print("Element not found")

if __name__ == "__main__":
    options, uiRoot = setUp()
    tap_element(options, uiRoot)
