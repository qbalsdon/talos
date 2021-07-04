#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from common import *
import unittest

class TestCommon(unittest.TestCase):

    DEVICE_NAME = "deviceName"

    def test_addAdb(self):
        test_input = ["devices"]
        expected = ["adb", "devices"]

        result = addAdb(test_input)

        self.assertEqual(result, expected)

    def test_addAdb_with_adb_in(self):
        test_input = ["adb", "devices"]
        expected = ["adb", "devices"]

        result = addAdb(test_input)

        self.assertEqual(result, expected)

    def test_addAdb_with_device(self):
        test_input = ["shell", "getprop"]
        expected = ["adb", "-s", self.DEVICE_NAME, "shell", "getprop"]

        result = addAdb(test_input, self.DEVICE_NAME)

        self.assertEqual(result, expected)

    def test_addAdb_with_device_already_specified(self):
        test_input = ["adb", "-s", self.DEVICE_NAME, "shell", "getprop"]
        expected = ["adb", "-s", self.DEVICE_NAME, "shell", "getprop"]

        result = addAdb(test_input, self.DEVICE_NAME)

        self.assertEqual(result, expected)

    def test_addAdb_with_device_already_specified_no_adb(self):
        test_input = ["-s", self.DEVICE_NAME, "shell", "getprop"]
        expected = ["adb", "-s", self.DEVICE_NAME, "shell", "getprop"]

        result = addAdb(test_input, self.DEVICE_NAME)

        self.assertEqual(result, expected)

    def test_value_for_param(self):
        self.assertEqual(valueForParam(["-s", "device"], "-s"), "device")

    def test_value_for_param_wrong_order(self):
        self.assertEqual(valueForParam(["device", "-s"], "-s"), None)

    def test_value_for_param_empty(self):
        self.assertEqual(valueForParam([], "-s"), None)

    def test_process_command_line_args_device(self):
        result = proccessArgs(["caller.py", "-s", "deviceName"])
        self.assertEqual(result.get("preferredDevice"), "deviceName")

    def test_process_command_line_args_no_device(self):
        result = proccessArgs(["caller.py"])
        self.assertFalse("device" in result)

    def test_process_command_line_args_element(self):
        result = proccessArgs(["caller.py", "-e", "elementName", "-s", "deviceName"])
        self.assertEqual(result.get("element"), "elementName")
        
if __name__ == "__main__":
    unittest.main()
