# -*- coding: utf-8 -*-
"""
test_test_travis
----------------------------------

Tests for `test_travis` module.
"""
import test_travis


def test_sayhello():
    assert test_travis.sayhello('Gaetano') == "Hello Gaetano!"
