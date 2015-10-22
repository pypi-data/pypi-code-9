# EFILTER Forensic Query Language
#
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

"""
EFILTER query type inference.
"""

__author__ = "Adam Sindelar <adamsh@google.com>"

from efilter import dispatch
from efilter import errors
from efilter import ast
from efilter import protocol
from efilter import query as q

from efilter.protocols import associative
from efilter.protocols import boolean
from efilter.protocols import reflective


@dispatch.multimethod
def infer_type(expr, scope=None):
    """Determines the types of each subexpression and validates sanity."""
    _ = expr, scope
    raise NotImplementedError()


@infer_type.implementation(for_type=q.Query)
def infer_type(query, scope=None):
    try:
        return infer_type(query.root, scope)
    except errors.EfilterError as error:
        error.query = query.source
        raise


@infer_type.implementation(for_type=ast.Literal)
def infer_type(expr, scope):
    _ = scope
    return type(expr.value)


@infer_type.implementation(for_type=ast.Binding)
def infer_type(expr, scope):
    if scope:
        result = reflective.reflect(scope, expr.value)

        if result:
            return result

    return protocol.AnyType


@infer_type.implementation(for_type=ast.Complement)
def infer_type(expr, scope):
    t = infer_type(expr.value, scope)
    if not protocol.isa(t, boolean.IBoolean):
        raise errors.EfilterTypeError(root=expr,
                                      actual=t,
                                      expected=boolean.IBoolean)

    return bool


@infer_type.implementation(for_type=ast.IsInstance)
def infer_type(expr, scope):
    _ = expr, scope
    return bool


@infer_type.implementation(for_type=ast.BinaryExpression)
def infer_type(expr, scope):
    lhs_type = infer_type(expr.lhs, scope)
    if not (lhs_type is protocol.AnyType
            or protocol.isa(lhs_type, expr.type_signature[0])):
        raise errors.EfilterTypeError(root=expr.lhs,
                                      expected=expr.type_signature[0],
                                      actual=lhs_type)

    rhs_type = infer_type(expr.rhs, scope)
    if not (lhs_type is protocol.AnyType
            or protocol.isa(rhs_type, expr.type_signature[1])):
        raise errors.EfilterTypeError(root=expr.rhs,
                                      expected=expr.type_signature[1],
                                      actual=rhs_type)

    return expr.return_signature


@infer_type.implementation(for_type=ast.VariadicExpression)
def infer_type(expr, scope):
    for subexpr in expr.children:
        t = infer_type(subexpr, scope)
        if not (t is protocol.AnyType
                or protocol.isa(t, expr.type_signature)):
            raise errors.EfilterTypeError(root=subexpr,
                                          expected=expr.type_signature,
                                          actual=t)

    return expr.return_signature


@infer_type.implementation(for_type=ast.Within)
def infer_type(expr, scope):
    t = infer_type(expr.context, scope)
    if not (t is protocol.AnyType
            or protocol.isa(t, associative.IAssociative)):
        raise errors.EfilterTypeError(root=expr,
                                      actual=t,
                                      expected=associative.IAssociative)

    return infer_type(expr.expression, t)


@infer_type.implementation(for_type=ast.Any)
def infer_type(expr, scope):
    t = infer_type(expr.context, scope)
    if not protocol.isa(t, boolean.IBoolean):
        raise errors.EfilterTypeError(root=expr,
                                      actual=t,
                                      expected=boolean.IBoolean)

    return bool


@infer_type.implementation(for_type=ast.Each)
def infer_type(expr, scope):
    t = infer_type(expr, scope)
    if not protocol.isa(t, boolean.IBoolean):
        raise errors.EfilterTypeError(root=expr,
                                      actual=t,
                                      expected=boolean.IBoolean)

    return bool
