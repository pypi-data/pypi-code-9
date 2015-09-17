#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_less2sass
----------------------------------

Tests for `less2sass` module.
"""

import unittest

from less2sass import less2sass


class TestLess2sassVariables(unittest.TestCase):
    """
    Test for how variables are represented in less and sass
    """

    def setUp(self):
        pass

    def test_variables(self):
        """https://gist.github.com/chriseppstein/674726#variables #1"""
        less = """@color: red;
        div {
          color: @color;
        }"""
        sass = """$color: red;
        div {
          color: $color;
        }"""
        less_conv = less2sass.replace_identifiers(less)
        self.assertEqual(sass, less_conv)

    def test_variables_scoped(self):
        """https://gist.github.com/chriseppstein/674726#variables #2"""
        less = """@color: black;
        .scoped {
          @bg: blue;
          @color: white;
          color: @color;
          background-color: @bg;
        }"""
        sass = """$color: black;
        .scoped {
          $bg: blue;
          $color: white;
          color: $color;
          background-color: $bg;
        }"""
        less_conv = less2sass.replace_identifiers(less)
        self.assertEqual(sass, less_conv)

    def test_variables_unscoped(self):
        """https://gist.github.com/chriseppstein/674726#variables #3"""
        less = """@color: black;
        .unscoped {
          color: @color;
          // Would be Error
        }"""
        sass = """$color: black;
        .unscoped {
          color: $color;
          // Would be Error
        }"""
        less_conv = less2sass.replace_identifiers(less)
        self.assertEqual(sass, less_conv)

    def tearDown(self):
        pass


class TestLess2sassNestedSelectors(unittest.TestCase):
    """
    Tesing nested selectors, currently this is a filler test case as there is
    no diference between nested selectors in sass ans less
    """

    def setUp(self):
        pass

    def test_nested_selectors(self):
        """https://gist.github.com/chriseppstein/674726#nested-selectors"""
        less = """p {
          a {
            color: red;
            &:hover {
              color: blue;
            }
          }
        }"""
        sass = """p {
          a {
            color: red;
            &:hover {
              color: blue;
            }
          }
        }"""
        less_conv = less
        self.assertEqual(sass, less_conv)

    def tearDown(self):
        pass


class TestLess2sassMixins(unittest.TestCase):
    """
    Test for mixins
    """

    def setUp(self):
        pass

    def test_mixins(self):
        """https://gist.github.com/chriseppstein/674726#mixins"""
        less = """.bordered {
          border-top: dotted 1px black;
          border-bottom: solid 2px black;
        }

        #menu a {
          .bordered;
        }"""
        sass = """@mixin bordered {
          border-top: dotted 1px black;
          border-bottom: solid 2px black;
        }

        #menu a {
          @include bordered;
        }"""
        less_conv_ = less2sass.replace_identifiers(less)
        less_conv = less2sass.replace_mixins(less_conv_)
        self.assertEqual(sass, less_conv)

    def test_mixins_dynamic(self):
        """https://gist.github.com/chriseppstein/674726#mixins-with-arguments--dynamic-mixins"""  # NOQA
        less = """.bordered(@width: 2px) {
          border: @width solid black;
        }

        #menu a {
          .bordered(4px);
        }"""
        sass = """@mixin bordered($width: 2px) {
          border: $width solid black;
        }

        #menu a {
          @include bordered(4px);
        }"""
        less_conv_ = less2sass.replace_identifiers(less)  # as there are id's
        less_conv = less2sass.replace_mixins(less_conv_)
        self.assertEqual(sass, less_conv)

    def tearDown(self):
        pass
