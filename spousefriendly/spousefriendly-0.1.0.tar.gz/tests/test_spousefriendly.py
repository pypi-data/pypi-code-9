#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_spousefriendly
----------------------------------

Tests for `spousefriendly` module.
"""

import unittest

import mock
import spousefriendly


SUCCESS_BOX_CALLABLE = 'easygui.msgbox'
FAILURE_BOX_CALLABLE = 'easygui.codebox'


def gui_mode():
    return spousefriendly.RunningMode.gui


class TestSpousefriendly(unittest.TestCase):

    # It's hard to test the actual GUI stuff. But we can check the right
    # path is taken, mocking out easygui

    def test_friendly_success_success_path(self):
        with mock.patch('spousefriendly.running_mode', new=gui_mode):
            with mock.patch(SUCCESS_BOX_CALLABLE) as msgbox:
                with spousefriendly.friendly_success():
                    1 + 1

        msgbox.assert_called_once_with("Script setup.py completed successfully.")

    def test_friendly_success_failure_path(self):
        try:
            with mock.patch('spousefriendly.running_mode', new=gui_mode):
                with mock.patch(SUCCESS_BOX_CALLABLE) as msgbox:
                    with spousefriendly.friendly_success():
                        1 / 0
        except ZeroDivisionError:
            pass

        msgbox.assert_not_called()

    def test_friendly_failure_success_path(self):
        with mock.patch('spousefriendly.running_mode', new=gui_mode):
            with mock.patch(FAILURE_BOX_CALLABLE) as errorbox:
                with spousefriendly.friendly_failure():
                    1 + 1

        errorbox.assert_not_called()

    def test_friendly_failure_failure_path(self):
        try:
            with mock.patch('spousefriendly.running_mode', new=gui_mode):
                with mock.patch(FAILURE_BOX_CALLABLE) as errorbox:
                    with spousefriendly.friendly_failure():
                        1 / 0
        except ZeroDivisionError:
            pass

        self.assertEqual(errorbox.call_count, 1)

    def test_friendly_success_and_failure_success_path(self):
        # Test how the two compose
        with mock.patch('spousefriendly.running_mode', new=gui_mode):
            with mock.patch(SUCCESS_BOX_CALLABLE) as msgbox:
                with mock.patch(FAILURE_BOX_CALLABLE) as errorbox:
                    with spousefriendly.friendly_success_and_failure():
                        1 + 1

        self.assertEqual(msgbox.call_count, 1)
        self.assertEqual(errorbox.call_count, 0)

    def test_friendly_success_and_failure_failure_path(self):
        try:
            with mock.patch('spousefriendly.running_mode', new=gui_mode):
                with mock.patch(SUCCESS_BOX_CALLABLE) as msgbox:
                    with mock.patch(FAILURE_BOX_CALLABLE) as errorbox:
                        with spousefriendly.friendly_success_and_failure():
                            1 / 0
        except ZeroDivisionError:
            pass

        self.assertEqual(msgbox.call_count, 0)
        self.assertEqual(errorbox.call_count, 1)
