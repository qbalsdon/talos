#!/usr/bin/env python3
import sys
from simplifier import setUp
from animation import validateArgs
from common import adbCommand, adbGetValue, adbSetValue, alternator, sysprops_transaction

show_touch_usage="""
  show_touch.py [-s __DEVICE__] [-t, --toggle, --on, --off]
"""

def modify_touch(new_value, device):
    adbSetValue("system", "show_touches", new_value, device)
    # technically do not need unless you are already on the settings screen
    sysprops_transaction(device)

def get_touch_state(device):
    return adbGetValue("system", "show_touches", device)

def touch_dictionary(device):
    return {
         "0": lambda: modify_touch("0", device),
         "1": lambda: modify_touch("1", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    desired_value = validateArgs(args, show_touch_usage)
    alternator(lambda: get_touch_state(device), touch_dictionary(device), desired_value)
