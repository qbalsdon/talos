#!/usr/bin/env python3
import os
import unicodedata
from common import adbCommand
from simplifier import setUp

"""
adb -s $DEVICE shell settings list secure > $SECURE_FILE1
adb -s $DEVICE shell settings list global > $GLOBAL_FILE1
adb -s $DEVICE shell settings list system > $SYSTEM_FILE1
"""

def attempt_numeric_conversion(possible_number):
    try:
        return float(possible_number)
    except ValueError:
        pass
    try:
        return unicodedata.numeric(possible_number)
    except (TypeError, ValueError):
        pass

    return possible_number

def convert_settings_to_dictionary(file_contents):
    return_dict = {}
    for line in file_contents.splitlines():
        if len(line) == 0:
            continue
        values = line.split("=")
        return_dict[values[0]] = attempt_numeric_conversion(values[1])

    return return_dict

def get_diff(data_set_one, data_set_two):
    # return_dict = { k : data_set_two[k] for k in set(data_set_two) - set(data_set_one) }
    return_dict = {}
    for key in set(data_set_two):
        if key not in data_set_one:
            return_dict[key] = [None, data_set_two[key]]
        elif data_set_one[key] != data_set_two[key]:
            return_dict[key] = [data_set_one[key], data_set_two[key]]
    return return_dict

def consolodate_diff(original_diff, new_diff):
    return_dict = original_diff.copy()
    for key in set(new_diff):
        key_array = new_diff[key]
        if key not in return_dict:
            return_dict[key] = key_array
        else:
            for element in key_array:
                if element not in return_dict[key]:
                    return_dict[key] = return_dict[key] + [element]
    return return_dict

def read_settings(settings_name, device):
    return convert_settings_to_dictionary(adbCommand(["shell", "settings", "list", settings_name], device))

def pretty_print_section(title, payload):
    result = ""
    if payload != None and len(payload) > 0:
        result = title
        for key in payload:
            result = result + "\n    " + key + " ["
            for element in payload[key]:
                if isinstance(element, str):
                    result = result + "'" + str(element) + "', "
                else:
                    result = result + str(element) + ", "
            result = result[:-2] + "]"
    return result

def pretty_print(secure_payload, global_payload, system_payload):
    result = ""
    secure_out = pretty_print_section("SECURE", secure_payload)
    global_out = pretty_print_section("GLOBAL", global_payload)
    system_out = pretty_print_section("SYSTEM", system_payload)

    if (secure_out != ""):
        result = result + secure_out + "\n"
    if (global_out != ""):
        result = result + global_out + "\n"
    if (system_out != ""):
        result = result + system_out + "\n"

    return result

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    secure_diff = {}
    global_diff = {}
    system_diff = {}
    secure_baseline = read_settings("secure", device)
    global_baseline = read_settings("global", device)
    system_baseline = read_settings("system", device)

    output = "NO CHANGES"
    while True:
        secure_diff = consolodate_diff(secure_diff, get_diff(secure_baseline, read_settings("secure", device)))
        global_diff = consolodate_diff(global_diff, get_diff(global_baseline, read_settings("global", device)))
        system_diff = consolodate_diff(system_diff, get_diff(system_baseline, read_settings("system", device)))
        new_output = pretty_print(secure_diff, global_diff, system_diff)
        if new_output != output:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            output = new_output
            print(output)
