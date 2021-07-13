#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from flip import *

class TestFlip(unittest.TestCase):
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

    def test_validateArgs_toggle_returns_toggle(self):
        try:
            result = validateArgs(["-s","--portrait", "--toggle"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_t_returns_toggle(self):
        try:
            result = validateArgs(["-s","--portrait", "-t"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_l_returns_landscape(self):
        try:
            result = validateArgs(["-l"])
            self.assertEqual(result, 1)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_landscape_returns_landscape(self):
        try:
            result = validateArgs(["--landscape"])
            self.assertEqual(result, 1)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_p_returns_landscape(self):
        try:
            result = validateArgs(["-p"])
            self.assertEqual(result, 0)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_portrait_returns_portrait(self):
        try:
            result = validateArgs(["--portrait"])
            self.assertEqual(result, 0)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_fails_with_conflict(self):
        try:
            result = validateArgs(["-p", "-l"])
            self.fail("Should fail with conflicting arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_fails_with_unknown(self):
        try:
            result = validateArgs(["--weird"])
            self.fail("Should fail with conflicting arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
