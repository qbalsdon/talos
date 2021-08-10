#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

'''
Usage:
    swipe [-s DEVICE] [-u|-d|-l|-r] [-c LENGTH]
'''

from swipe import validateArgs, percent_length, determine_swipe_points

class TestSwipe(unittest.TestCase):
    def test_validateArgs_device_only_valid_inputs(self):
        valid_args = {
            "-u": "u",
            "-d": "d",
            "-l": "l",
            "-r": "r"
        }
        try:
            #the device could have this name
            result = validateArgs(["-s","--devicename"])
            self.assertEqual(result, "u")
        except Exception as e:
            self.fail("Should pass with no arguments")

        try:
            #the device could have this name
            result = validateArgs()
            self.assertEqual(result, "u")
        except Exception as e:
            self.fail("Should pass with no arguments")

        for key in valid_args:
            try:
                #the device could have this name
                result = validateArgs(["-s","--devicename", key])
                self.assertEqual(result, valid_args[key])
            except Exception as e:
                self.fail("WITH DEVICE: Should pass with no arguments")

            try:
                #the device could have this name
                result = validateArgs([key])
                self.assertEqual(result, valid_args[key])
            except Exception as e:
                self.fail("NO DEVICE: Should pass with no arguments")

    def test_validateArgs_device_fail_multiple_inputs(self):
        try:
            #the device could have this name
            result = validateArgs(["-s","--portrait", "-u", "-l"])
            self.fail("Should fail with many arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_device_fail_incorrect(self):
        try:
            #the device could have this name
            result = validateArgs(["-s","--portrait", "-k"])
            self.fail("Should fail with incorrect arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_percent_length(self):
        test_subject = percent_length(100, 75)
        self.assertEqual(test_subject, 75)

    def test_swipe_left(self):
        screen_size = {'width': 1080, 'height': 2340}
        self.assertEqual(determine_swipe_points(screen_size, "l", 75), (945, 1170, 135, 1170))

    def test_swipe_right(self):
        screen_size = {'width': 1080, 'height': 2340}
        self.assertEqual(determine_swipe_points(screen_size, "r", 75), (135, 1170, 945, 1170))

    def test_swipe_up(self):
        screen_size = {'width': 1080, 'height': 2340}
        self.assertEqual(determine_swipe_points(screen_size, "u", 75), (540, 2047, 540, 292))

    def test_swipe_down(self):
        screen_size = {'width': 1080, 'height': 2340}
        self.assertEqual(determine_swipe_points(screen_size, "d", 75), (540, 292, 540, 2047))

if __name__ == "__main__":
    unittest.main()
