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

def press_button(keycode, device):
    adbCommand(["shell", "input", "keyevent", keycode], device)

def type_text(text, device):
    adbCommand(["shell", "input", "text", text.replace(" ", "\ ")], device)

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
        "xml": "-x",
        "percent": "-p",
        "text": "-t"
    }

    options = {}

    for key in optionals:
        value = valueForParam(args, optionals[key])
        if value != None:
            options[key] = value

    return options

def alternator(read_function, change_dictionary, desired_value=None):
    value = read_function()
    if value == None:
        raise RuntimeError("read_function requires a return value")
    if value != desired_value:
        if desired_value == None:
            #toggle / strafe
            keys_array = list(change_dictionary)
            try:
                current_index = keys_array.index(value)
            except Exception as e:
                output="["
                for key in keys_array:
                    output+= str(key) + ": (" + str(type(key)) +"), "
                print("~~~~> Looking for value " + str(value) + " (" + str(type(value)) + ")" + " in keys:")
                print(output[:-2] + "]")
                raise e
            next_index = (current_index + 1) % len(keys_array)
            change_dictionary[keys_array[next_index]]()
        else:
            change_dictionary[desired_value]()
        return True
    else:
        return False

if __name__ == "__main__":
    print("!! Common is a library !!")
    print(proccessArgs())
