#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from common import alternator

"""
Reads value
3 Options:
 - It's the value we want: do nothing
 - It's NOT the value we want: change it
 - We want to toggle it: change it
"""

class TestAlternator(unittest.TestCase):
    #helper methods
    def methodReadNullReturn(self):
        self.hasBeenRead = True

    def methodChange(self, value):
        self.hasBeenChanged = True
        self.valueSet = value

    def methodChangeFromFive(self):
        self.methodCallCount = self.methodCallCount + 1
        self.hasBeenChanged = True
        self.valueSet = 7

    def methodChangeFromSeven(self):
        self.methodCallCount = self.methodCallCount + 1
        self.hasBeenChanged = True
        self.valueSet = 5

    def methodRead(self):
        self.hasBeenRead = True
        return 5

    def methodReadDynamic(self):
        self.hasBeenRead = True
        return self.valueSet

    #runs before each test
    def setUp(self):
        self.methodCallCount = 0
        self.hasBeenRead = False
        self.hasBeenChanged = False
        self.valueSet = None
        self.lamda_dictionary = {
             5: self.methodChangeFromFive,
             7: self.methodChangeFromSeven
        }

    #actual tests
    def test_value_is_read(self):
        result = alternator(self.methodRead, self.lamda_dictionary, 5)
        self.assertTrue(self.hasBeenRead)

    def test_value_is_read_throws_if_null(self):
        try:
            result = alternator(self.methodReadNullReturn, self.lamda_dictionary)
            self.assertFalse(self.hasBeenChanged)
            self.fail("This should not be passing: ValueError expected")
        except Exception as e:
            self.assertTrue(e.__class__ is RuntimeError)
        self.assertFalse(self.hasBeenChanged)

    def test_value_not_changed_if_same(self):
        self.assertFalse(self.hasBeenRead)
        result = alternator(self.methodRead, self.lamda_dictionary, 5)
        self.assertFalse(result)
        self.assertTrue(self.hasBeenRead)
        self.assertFalse(self.hasBeenChanged)

    def test_value_changed_if_different(self):
        self.assertFalse(self.hasBeenRead)
        self.assertFalse(self.hasBeenChanged)
        result = alternator(self.methodRead, self.lamda_dictionary, 7)
        self.assertTrue(result)
        self.assertTrue(self.hasBeenRead)
        self.assertTrue(self.hasBeenChanged)
        self.assertEqual(self.valueSet, 5)

    def test_value_changed_always_when_no_value_sent(self):
        self.valueSet = 5
        self.assertFalse(self.hasBeenRead)
        self.assertFalse(self.hasBeenChanged)
        result = alternator(self.methodReadDynamic, self.lamda_dictionary)
        self.assertTrue(result)
        self.assertTrue(self.hasBeenRead)
        self.assertTrue(self.hasBeenChanged)
        self.assertEqual(self.valueSet, 7)
        self.assertEqual(self.methodCallCount, 1)
        self.hasBeenRead = False
        self.hasBeenChanged = False
        result = alternator(self.methodReadDynamic, self.lamda_dictionary)
        self.assertTrue(result)
        self.assertTrue(self.hasBeenRead)
        self.assertTrue(self.hasBeenChanged)
        self.assertEqual(self.valueSet, 5)
        self.assertEqual(self.methodCallCount, 2)

if __name__ == "__main__":
    unittest.main()
