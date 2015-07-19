# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for yapf.subtype_assigner."""

import sys
import textwrap
import unittest

from yapf.yapflib import format_token
from yapf.yapflib import pytree_unwrapper
from yapf.yapflib import pytree_utils
from yapf.yapflib import pytree_visitor
from yapf.yapflib import subtype_assigner


class SubtypeAssignerTest(unittest.TestCase):

  def _ParseAndUnwrap(self, code, dumptree=False):
    """Produces unwrapped lines from the given code.

    Parses the code into a tree, assigns subtypes and runs the unwrapper.

    Arguments:
      code: code to parse as a string
      dumptree: if True, the parsed pytree (after comment splicing) is dumped
        to stderr. Useful for debugging.

    Returns:
      List of unwrapped lines.
    """
    tree = pytree_utils.ParseCodeToTree(code)
    subtype_assigner.AssignSubtypes(tree)

    if dumptree:
      pytree_visitor.DumpPyTree(tree, target_stream=sys.stderr)

    return pytree_unwrapper.UnwrapPyTree(tree)

  def _CheckFormatTokenSubtypes(self, uwlines, list_of_expected):
    """Check that the tokens in the UnwrappedLines have the expected subtypes.

    Args:
      uwlines: list of UnwrappedLine.
      list_of_expected: list of (name, subtype) pairs. Non-semantic tokens are
        filtered out from the expected values.
    """
    actual = []
    for uwl in uwlines:
      filtered_values = [(ft.value, ft.subtype) for ft in uwl.tokens
                         if ft.name not in pytree_utils.NONSEMANTIC_TOKENS]
      if filtered_values:
        actual.append(filtered_values)

    self.assertEqual(list_of_expected, actual)

  def testFuncDefDefaultAssign(self):
    code = textwrap.dedent(r"""
        def foo(a=37, *b, **c):
          return -x[:42]
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('def', format_token.Subtype.NONE),
         ('foo', format_token.Subtype.NONE),
         ('(', format_token.Subtype.NONE),
         ('a', format_token.Subtype.NONE),
         ('=', format_token.Subtype.DEFAULT_OR_NAMED_ASSIGN),
         ('37', format_token.Subtype.NONE),
         (',', format_token.Subtype.NONE),
         ('*', format_token.Subtype.VARARGS_STAR),
         ('b', format_token.Subtype.NONE),
         (',', format_token.Subtype.NONE),
         ('**', format_token.Subtype.KWARGS_STAR_STAR),
         ('c', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         (':', format_token.Subtype.NONE)],
        [('return', format_token.Subtype.NONE),
         ('-', format_token.Subtype.UNARY_OPERATOR),
         ('x', format_token.Subtype.NONE),
         ('[', format_token.Subtype.NONE),
         (':', format_token.Subtype.SUBSCRIPT_COLON),
         ('42', format_token.Subtype.NONE),
         (']', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testFuncCallWithDefaultAssign(self):
    code = textwrap.dedent(r"""
        foo(x, a='hello world')
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('foo', format_token.Subtype.NONE),
         ('(', format_token.Subtype.NONE),
         ('x', format_token.Subtype.NONE),
         (',', format_token.Subtype.NONE),
         ('a', format_token.Subtype.NONE),
         ('=', format_token.Subtype.DEFAULT_OR_NAMED_ASSIGN),
         ("'hello world'", format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testSetComprehension(self):
    code = textwrap.dedent("""\
        def foo(strs):
          return {s.lower() for s in strs}
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('def', format_token.Subtype.NONE),
         ('foo', format_token.Subtype.NONE),
         ('(', format_token.Subtype.NONE),
         ('strs', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         (':', format_token.Subtype.NONE)],
        [('return', format_token.Subtype.NONE),
         ('{', format_token.Subtype.NONE),
         ('s', format_token.Subtype.NONE),
         ('.', format_token.Subtype.NONE),
         ('lower', format_token.Subtype.NONE),
         ('(', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         ('for', format_token.Subtype.DICT_SET_GENERATOR),
         ('s', format_token.Subtype.NONE),
         ('in', format_token.Subtype.NONE),
         ('strs', format_token.Subtype.NONE),
         ('}', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testUnaryNotOperator(self):
    code = textwrap.dedent("""\
        not a
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('not', format_token.Subtype.UNARY_OPERATOR),
         ('a', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testBitwiseOperators(self):
    code = textwrap.dedent("""\
        x = ((a | (b ^ 3) & c) << 3) >> 1
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('x', format_token.Subtype.NONE),
         ('=', format_token.Subtype.ASSIGN_OPERATOR),
         ('(', format_token.Subtype.NONE),
         ('(', format_token.Subtype.NONE),
         ('a', format_token.Subtype.NONE),
         ('|', format_token.Subtype.BINARY_OPERATOR),
         ('(', format_token.Subtype.NONE),
         ('b', format_token.Subtype.NONE),
         ('^', format_token.Subtype.BINARY_OPERATOR),
         ('3', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         ('&', format_token.Subtype.BINARY_OPERATOR),
         ('c', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         ('<<', format_token.Subtype.BINARY_OPERATOR),
         ('3', format_token.Subtype.NONE),
         (')', format_token.Subtype.NONE),
         ('>>', format_token.Subtype.BINARY_OPERATOR),
         ('1', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testSubscriptColon(self):
    code = textwrap.dedent("""\
        x[0:42:1]
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('x', format_token.Subtype.NONE),
         ('[', format_token.Subtype.NONE),
         ('0', format_token.Subtype.NONE),
         (':', format_token.Subtype.SUBSCRIPT_COLON),
         ('42', format_token.Subtype.NONE),
         (':', format_token.Subtype.SUBSCRIPT_COLON),
         ('1', format_token.Subtype.NONE),
         (']', format_token.Subtype.NONE)]
    ])  # yapf: disable

  def testFunctionCallWithStarExpression(self):
    code = textwrap.dedent("""\
        [a, *b]
        """)
    uwlines = self._ParseAndUnwrap(code)
    self._CheckFormatTokenSubtypes(uwlines, [
        [('[', format_token.Subtype.NONE),
         ('a', format_token.Subtype.NONE),
         (',', format_token.Subtype.NONE),
         ('*', format_token.Subtype.UNARY_OPERATOR),
         ('b', format_token.Subtype.NONE),
         (']', format_token.Subtype.NONE)]
    ])  # yapf: disable


if __name__ == '__main__':
  unittest.main()
