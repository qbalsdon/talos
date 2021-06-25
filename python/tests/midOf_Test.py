#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from midOf import *
from fetchUI import *

import unittest
from testdata import *

class TestMidOf(unittest.TestCase):

    DEVICE_NAME = "deviceName"

    def test_validateArgs_none(self):
        try:
            validateArgs(None)
            self.fail("validateArgs should have thrown ValueError - parameters cannot be null")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_empty(self):
        try:
            validateArgs({})
            self.fail("validateArgs should have thrown ValueError - parameters cannot be empty")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_element(self):
        self.assertTrue(validateArgs({"element": "elementName"}))

    def test_validateArgs_property_no_value(self):
        try:
            validateArgs({"property": "propertyValue"})
            self.fail("validateArgs should have thrown ValueError - property with no value")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_with_file(self):
        try:
            validateArgs({"property": "propertyValue"})
            self.fail("validateArgs should have thrown ValueError - property with no value")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_property_and_value(self):
        self.assertTrue(validateArgs({"property": "propertyValue", "value": "valueText"}))

    def test_midOf_element(self):
        result = midOf({"element": "RUN CURRENT DEBUG ACTION"}, parseXML(data = testData))
        self.assertEqual(result, {'x': 540.0, 'y': 942.0})

    def test_midOf_element_partial(self):
        result = midOf({"element": "rent deb"}, parseXML(data = testData))
        self.assertEqual(result, {'x': 540.0, 'y': 942.0})

    def test_midOf_property_partial(self):
        result = midOf({"property": "resource-id", "value": "volumeLabel"}, parseXML(data = testData))
        self.assertEqual(result, {'x': 539.0, 'y': 797.0})

if __name__ == "__main__":
    unittest.main()
