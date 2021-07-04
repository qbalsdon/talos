#!/usr/bin/env python3
import subprocess
import sys

def addAdb(parameters, device=None):
    params = parameters

    #check for adb
    if params[0] != "adb":
        params = ["adb"] + params

    # check for device flag
    if device != None and params[1] != "-s":
        params = [params[0]] + ["-s", str(device)] + params[1:]
    return params

def adbCommand(parameters, device=None, output=True):
    command_params=addAdb(parameters, device)
    if output:
        return subprocess.run(command_params, capture_output=True).stdout.decode().strip()
    else:
        subprocess.run(command_params, capture_output=True)
    return ""

def adbGetValue(level, variable_name, device=None, output=True):
    command_params=addAdb(["shell", "settings", "get", level, variable_name], device)
    value = subprocess.run(command_params, capture_output=True).stdout.decode().strip()
    return value

def adbSetValue(level, variable_name, value, device=None, output=True):
    command_params=addAdb(["shell", "settings", "put", level, variable_name, value], device)
    subprocess.run(command_params, capture_output=True)

def valueForParam(args, param):
    if len(args) == 0 or not param in args:
        return None
    index = args.index(param)
    if index >= 0 and index + 1 < len(args):
        return args[index + 1]
    return None

def proccessArgs(args = None):
    if args == None:
        args = sys.argv
    optionals = {
        "preferredDevice" : "-s",
        "element" : "-e",
        "property" : "-prop",
        "value" : "-v",
        "file": "-f",
        "xml": "-x"
    }

    options = {}

    for key in optionals:
        value = valueForParam(args, optionals[key])
        if value != None:
            options[key] = value

    return options

def toggle_value(desired_value, accessor, modifier):
    current_value = accessor()
    changed = False
    if current_value != desired_value:
        modifier()
        changed = True
    return changed

if __name__ == "__main__":
    print("!! Common is a library !!")
    print(proccessArgs())
