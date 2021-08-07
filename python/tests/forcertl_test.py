#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

'''
Settings
    GLOBAL debug.force_rtl [0.0, 1.0]

Usage:
    force_rtl
'''

from forcertl import *

class TestForceRtl(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
