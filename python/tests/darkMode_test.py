#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from darkMode import validateArgs, change_required


class TestDarkMode(unittest.TestCase):
    def test_validate_args(self):
        self.assertEqual(validateArgs(None), None)
        self.assertEqual(validateArgs([]), None)
        self.assertEqual(validateArgs(["-t"]), None)
        self.assertEqual(validateArgs(["--toggle"]), None)
        self.assertEqual(validateArgs(["-d"]), "dark")
        self.assertEqual(validateArgs(["--dark"]), "dark")
        self.assertEqual(validateArgs(["-l"]), "light")
        self.assertEqual(validateArgs(["--light"]), "light")

        self.assertEqual(validateArgs(["-s","device"]), None)
        self.assertEqual(validateArgs(["-s","device", "-t"]), None)
        self.assertEqual(validateArgs(["-s","device", "--toggle"]), None)
        self.assertEqual(validateArgs(["-s","device", "-d"]), "dark")
        self.assertEqual(validateArgs(["-s","device", "--dark"]), "dark")
        self.assertEqual(validateArgs(["-s","device", "-l"]), "light")
        self.assertEqual(validateArgs(["-s","device", "--light"]), "light")

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
            validateArgs(["-s","device", "-l", "-d"])
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def state_dark(self, unused):
        return 2

    def state_light(self, unused):
        return 1

    def test_change_required(self):
        self.assertTrue(change_required("unused", None, read_state=lambda device: self.state_light(device)))
        self.assertTrue(change_required("unused", "dark", read_state=lambda device: self.state_light(device)))
        self.assertTrue(change_required("unused", "light", read_state=lambda device: self.state_dark(device)))
        self.assertFalse(change_required("unused", "dark", read_state=lambda device: self.state_dark(device)))
        self.assertFalse(change_required("unused", "light", read_state=lambda device: self.state_light(device)))

    def test_change_required_fails(self):
        try:
            change_required("unused", "None", read_state=lambda device: self.state_light(device))
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
