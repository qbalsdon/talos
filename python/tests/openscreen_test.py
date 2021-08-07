#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from openscreen import validateArgs, screen_options, activity_screens

class TestOpenScreen(unittest.TestCase):
    def test_validateArgs_none_fails(self):
        try:
            validateArgs(None)
            self.fail("Should fail with no arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_device_only_none_fails(self):
        try:
            validateArgs(["-s", "DEVICE_NAME"])
            self.fail("Should fail with no arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_empty_fails(self):
        try:
            validateArgs([])
            self.fail("Should fail with no arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_two_fails(self):
        try:
            validateArgs(["one","two"])
            self.fail("Should fail with no arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_unknown_fails(self):
        try:
            validateArgs(["unknown"])
            self.fail("Should fail with unknown argument")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_dark_passes(self):
        self.assertEqual("dark", validateArgs(["dark"]))

if __name__ == "__main__":
    unittest.main()
