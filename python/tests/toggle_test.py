#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from common import toggle_value
"""
Read a value
determine if we should toggle
   yes: toggle
   no:  ignore
"""

class TestToggle(unittest.TestCase):
    #runs before each test
    def setUp(self):
        self.shouldBeChangedToTrue = False
        self.shouldRemainFalse = False

    #helper methods
    def methodShouldChangeToTrue(self):
        self.shouldBeChangedToTrue = True

    def methodIfCalledIsAMistake(self):
        self.shouldBeFalse = True

    #actual tests
    def test_toggle_value_true_to_false(self):
        result = toggle_value(False, lambda : True, self.methodShouldChangeToTrue)
        self.assertTrue(result)
        self.assertTrue(self.shouldBeChangedToTrue)

    def test_toggle_value_false_to_true(self):
        result = toggle_value(True, lambda : False, self.methodShouldChangeToTrue)
        self.assertTrue(result)
        self.assertTrue(self.shouldBeChangedToTrue)

    def test_toggle_arbitrary_value(self):
        result = toggle_value(2, lambda : 1, self.methodShouldChangeToTrue)
        self.assertTrue(result)
        self.assertTrue(self.shouldBeChangedToTrue)

    def test_toggle_arbitrary_value_no_toggle(self):
        result = toggle_value(3, lambda : 3, self.methodIfCalledIsAMistake)
        self.assertFalse(result)
        self.assertFalse(self.shouldRemainFalse)

if __name__ == "__main__":
    unittest.main()
