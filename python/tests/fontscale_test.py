#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

'''
Settings
    SYSTEM font_scale [0.85, 1.0, 1.15, 1.3]

Usage:
    fontscale [ -t --toggle -sm --small -d --default -l --large -el --largest ]
'''

from fontscale import *

class TestFontScale(unittest.TestCase):

    def test_validateArgs_none_returns_toggle(self):
        try:
            self.assertEqual(validateArgs(), None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_empty_returns_toggle(self):
        try:
            result = validateArgs([])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_device_no_interference(self):
        try:
            #the device could have this name
            result = validateArgs(["-s","--portrait"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def check_parameter(self, parameter, expected, withDeviceParams = False):
        try:
            if withDeviceParams:
                result = validateArgs(["-s","--portrait", parameter])
            else:
                result = validateArgs([parameter])

            self.assertEqual(result, expected)
        except Exception as e:
            self.fail("Validate args with {} did not yield {} [DEVICEPARAMS: {}]".format(parameter, expected, withDeviceParams))

    def test_validateArgs_toggle_returns_toggle(self):
        argResults = {
            "-t" : None,
            "--toggle" : None,
            "-sm" : 0.85,
            "-small" : 0.85,
            "-d" : 1,
            "--defaul" : 1,
            "-l" : 1.15,
            "--large" : 1.15,
            "-el" : 1.3,
            "--largest" : 1.3
        }
        for element in argResults:
            self.check_parameter(element, argResults[element])
            self.check_parameter(element, argResults[element], True)

    def test_validateArgs_fails_with_conflict(self):
        try:
            result = validateArgs(["-p", "-l"])
            self.fail("Should fail with conflicting arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_fails_with_unknown(self):
        try:
            result = validateArgs(["--weird"])
            self.fail("Should fail with unkown arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
