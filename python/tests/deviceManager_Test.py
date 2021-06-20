#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from deviceManager import *

import unittest

class TestGetDevice(unittest.TestCase):
    #====== process_device ========
    def test_parse_happy_case(self):
        test_input = ["13021FDD4005XC	device", "emulator-5554	offline"]
        expected = [{'Name':'13021FDD4005XC','Status':'device'},{'Name':'emulator-5554','Status':'offline'}]

        self.assertEqual(process_device(test_input[0]), expected[0])
        self.assertEqual(process_device(test_input[1]), expected[1])

    def test_parse_fails(self):
        test_input = "Should fail"
        expected = None
        self.assertEqual(process_device(test_input), expected)
    #==============================

    #====== statusFilter =======
    def test_status_filter_with_device(self):
        test_input = {'Name':'emulator-5554','Status':'device'}
        result = statusFilter(test_input)
        self.assertTrue(result)

    def test_status_filter_with_unconnected_device(self):
        test_input = {'Name':'emulator-5554','Status':'offline'}
        result = statusFilter(test_input)
        self.assertFalse(result)
    #===========================

    #====== deviceFilter =======
    def test_device_filter_with_device(self):
        test_input = {'Name':'13021FDD4005XC','Status':'offline'}
        result = deviceFilter(test_input)
        self.assertTrue(result)

    def test_device_filter_with_emulator(self):
        test_input = {'Name':'emulator-5554','Status':'offline'}
        result = deviceFilter(test_input)
        self.assertFalse(result)
    #===========================

    #====== prefferedFilter =======
    def test_preferred_filter_with_device_connected(self):
        test_input = {'Name':'13021FDD4005XC_Test','Status':'device'}
        result = preferredFilter(test_input, "13021FDD4005XC_Test")
        self.assertTrue(result)

    def test_preferred_filter_with_device_disconnected(self):
        test_input = {'Name':'13021FDD4005XC_Test','Status':'offline'}
        result = preferredFilter(test_input, "13021FDD4005XC_Test")
        self.assertFalse(result)

    def test_preferred_filter_with_emulator(self):
        test_input = {'Name':'emulator-5554','Status':'offline'}
        result = preferredFilter(test_input, "13021FDD4005XC_Test")
        self.assertFalse(result)
    #===========================

    #======= getDevice =======
    def test_get_emulator_if_available(self):
        test_input = [{'Name':'emulator-5554','Status':'device'}, {'Name':'13021FDD4005XC','Status':'offline'}]
        expected = "emulator-5554"

        result = getDevice(test_input)

        self.assertEqual(result, expected)

    def test_exits_if_empty_devices(self):
        test_input = []
        expected = None

        print("\n~~~~ TESTING WITH EMPTY DEVICES ~~~~")
        result = getDevice(test_input)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.assertEqual(result, expected)

    def test_exits_if_no_active_devices(self):
        test_input = [{'Name':'emulator-5554','Status':'offline'}, {'Name':'13021FDD4005XC','Status':'offline'}]
        expected = None

        print("\n~~~~ TESTING WITH DISCONNECTED DEVICES ~~~~")
        result = getDevice(test_input)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.assertEqual(result, expected)

    def test_get_first_real_connected_device(self):
        test_input = [{'Name':'emulator-5554','Status':'device'}, {'Name':'13021FDD4005XC','Status':'device'}]
        expected = "13021FDD4005XC"

        result = getDevice(test_input)

        self.assertEqual(result, expected)

    def test_get_first_real_connected_device_prefer_os_default(self):
        test_input = [{'Name':'emulator-5554','Status':'device'}, {'Name':'13021FDD4005XC_fake','Status':'device'}, {'Name':'13021FDD4005XC_Test','Status':'device'}]
        expected = "13021FDD4005XC_Test"

        result = getDevice(deviceList = test_input, preferredDevice=expected)

        self.assertEqual(result, expected)

    def test_get_first_real_connected_device_prefer_os_default_but_default_not_connected(self):
        test_input = [{'Name':'emulator-5554','Status':'device'}, {'Name':'13021FDD4005XC_fake','Status':'device'}, {'Name':'13021FDD4005XC_test','Status':'offline'}]
        expected = "13021FDD4005XC_fake"

        result = getDevice(deviceList = test_input, preferredDevice="13021FDD4005XC_test")

        self.assertEqual(result, expected)

    #=========================

    #====== SCREEN SIZE ======
    def test_get_screen_size(self):
        test_input="""
        gvbrjkfnekjr
        """.strip()

        result = getScreenSize(test_input)

        expected = None

        self.assertEqual(result, expected)

    def test_get_screen_size(self):
        test_input="""
        Physical size: 1080x2340
        """.strip()

        result = getScreenSize(test_input)

        expected = {'width':1080, 'height':2340}

        self.assertEqual(result, expected)
    #=========================
if __name__ == "__main__":
    unittest.main()
