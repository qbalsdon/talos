#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from sysDiff import *
from testdata import secure_data_test

class TestSysDiff(unittest.TestCase):
    # def test_validateArgs_none_returns_toggle(self):
    #     try:
    #         self.assertEqual(validateArgs(), None)
    #     except Exception as e:
    #         self.fail("Should pass with no arguments")

    def test_try_numeric_conversion_0(self):
        test_data = "0"
        result = attempt_numeric_conversion(test_data)
        self.assertEqual(result, 0)

    def test_try_numeric_conversion_1(self):
        test_data = "1"
        result = attempt_numeric_conversion(test_data)
        self.assertEqual(result, 1)

    def test_try_numeric_conversion_long(self):
        test_data = "1625684972136"
        result = attempt_numeric_conversion(test_data)
        self.assertEqual(result, 1625684972136)

    def test_try_numeric_conversion_float(self):
        test_data = "2.0"
        result = attempt_numeric_conversion(test_data)
        self.assertEqual(result, 2.0)

    def test_try_numeric_conversion_string(self):
        test_data = "test string"
        result = attempt_numeric_conversion(test_data)
        self.assertEqual(result, "test string")

    def test_parse_file(self):
        result=convert_settings_to_dictionary(secure_data_test)
        self.assertEqual(len(result), 148)
        self.assertEqual(result["backup_enabled"], 0)
        self.assertEqual(result["usb_migration_state"], 0)
        self.assertEqual(result["voice_interaction_service"], "com.google.android.googlequicksearchbox/com.google.android.voiceinteraction.GsaVoiceInteractionService")
        self.assertEqual(result["accessibility_display_magnification_scale"], 2.0)

    def test_compare_data(self):
        data_set_one=convert_settings_to_dictionary(secure_data_test)
        data_set_two=convert_settings_to_dictionary(secure_data_test)
        data_set_two["backup_enabled"] = 1
        data_set_two["usb_migration_state"] = 2
        data_set_two["new_key"] = "test"

        result = get_diff(data_set_one, data_set_two)
        self.assertEqual(result["backup_enabled"], [0,1])
        self.assertEqual(result["usb_migration_state"], [0,2])
        self.assertEqual(result["new_key"], [None,"test"])

    def test_maintain_diffs_data(self):
        data_set_one=convert_settings_to_dictionary(secure_data_test)
        data_set_two=convert_settings_to_dictionary(secure_data_test)
        data_set_two["backup_enabled"] = 1
        data_set_two["usb_migration_state"] = 2
        data_set_two["new_key"] = "test1"

        diff1 = get_diff(data_set_one, data_set_two)
        test_subject = {}
        test_subject["usb_migration_state"] = [-1]
        test_subject["new_key"] = ["test0"]
        test_subject["old_remaining_change"] = ["value"]

        result = consolodate_diff(test_subject, diff1)
        self.assertEqual(result["backup_enabled"], [0,1])
        self.assertEqual(result["usb_migration_state"], [-1,0,2])
        self.assertEqual(result["new_key"], ["test0",None,"test1"])
        self.assertEqual(result["old_remaining_change"], ["value"])

    def test_pretty_print_section_empty(self):
        result = pretty_print_section("TEST", None)
        self.assertEqual(result, "")
        result = pretty_print_section("TEST", {})
        self.assertEqual(result, "")

    def test_pretty_print_section_single(self):
        result = pretty_print_section("TEST HEADING", {"test_data": [1]})
        expected = """
        TEST HEADING\n    test_data [1]""".strip()
        self.assertEqual(result, expected)
        result = pretty_print_section("TEST HEADING", {"test_data": [1, 0], "second_data": ["value1", "value2", "value3"]})
        expected = """TEST HEADING\n    test_data [1, 0]\n    second_data ['value1', 'value2', 'value3']""".strip()
        self.assertEqual(result, expected)

    def test_pretty_print_empty(self):
        result = pretty_print(None, None, None)
        self.assertEqual(result, "")
        result = pretty_print({}, {}, {})
        self.assertEqual(result, "")

    def test_pretty_print_just_one(self):
        expected = """SECURE\n    test_data [1, 0]\n    second_data ['value1', 'value2', 'value3']\n"""
        result = pretty_print({"test_data": [1, 0], "second_data": ["value1", "value2", "value3"]}, None, None)
        self.assertEqual(result, expected)

        expected = """GLOBAL\n    test_data [1, 0]\n    second_data ['value1', 'value2', 'value3']\n"""
        result = pretty_print(None, {"test_data": [1, 0], "second_data": ["value1", "value2", "value3"]}, None)
        self.assertEqual(result, expected)

        expected = """SYSTEM\n    test_data [1, 0]\n    second_data ['value1', 'value2', 'value3']\n"""
        result = pretty_print(None, None, {"test_data": [1, 0], "second_data": ["value1", "value2", "value3"]})
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
