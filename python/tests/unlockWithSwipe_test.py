#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from unlockWithSwipe import is_screen_on, ensure_screen_off, press_power

class TestAlternator(unittest.TestCase):
    #helpers
    def mock_settings_on(self, unused):
        return "Display Power: state=ON"

    def mock_settings_off(self, unused):
        return "Display Power: state=OFF"

    #actual tests
    def test_is_screen_on_with_on(self):
        result = is_screen_on("unused", self.mock_settings_on)
        self.assertTrue(result)

    def test_is_screen_on_with_off(self):
        result = is_screen_on("unused", self.mock_settings_off)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
