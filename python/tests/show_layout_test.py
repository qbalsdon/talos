#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from show_layout import validateArgs

class TestShowLayout(unittest.TestCase):
    def test_validate_args(self):
        self.assertEqual(validateArgs(None), None)
        self.assertEqual(validateArgs([]), None)
        self.assertEqual(validateArgs(["-t"]), None)
        self.assertEqual(validateArgs(["--toggle"]), None)
        self.assertEqual(validateArgs(["--on"]), "true")
        self.assertEqual(validateArgs(["--off"]), "false")

        self.assertEqual(validateArgs(["-s","device"]), None)
        self.assertEqual(validateArgs(["-s","device", "-t"]), None)
        self.assertEqual(validateArgs(["-s","device", "--toggle"]), None)
        self.assertEqual(validateArgs(["-s","device", "--on"]), "true")
        self.assertEqual(validateArgs(["-s","device", "--off"]), "false")

    def test_validate_args_invalid(self):
        try:
            validateArgs(["-s","device", "-p"])
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

        try:
            validateArgs(["-s","device", "hsdfkjd"])
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

        try:
            validateArgs(["-s","device", "--on", "--off"])
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
