#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from currentactivity import extract_activity
from testdata import dumpsys_window_displays

class TestCurrentActivity(unittest.TestCase):
    def test_gets_current_activity(self):
        self.assertEqual("com.android.vending/com.android.vending.AssetBrowserActivity", extract_activity(dumpsys_window_displays))

    def test_gets_current_activity_fails_with_none(self):
        try:
            extract_activity(None)
            self.fail("Should not work with None input")
        except Exception as e:
            self.assertTrue(e.__class__ is TypeError)

    def test_gets_current_activity_fails_with_blank(self):
        try:
            extract_activity("")
            self.fail("Should not work with Blank input")
        except Exception as e:
            self.assertTrue(e.__class__ is AttributeError)

    def test_gets_current_activity_fails_with_strange_input(self):
        try:
            extract_activity("Some janky input")
            self.fail("Should not work with Blank input")
        except Exception as e:
            self.assertTrue(e.__class__ is AttributeError)

if __name__ == "__main__":
    unittest.main()
