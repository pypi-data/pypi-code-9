"""This module contains definitions for the operators that are recognized by PXP programs."""

from pyebnf.operator import Association, Operator


# Arithmetic
op_add = Operator("+", 5)
op_subtract = Operator("-", 5)
op_multiply = Operator("*", 6)
op_divide = Operator("/", 6)
op_modulus = Operator("%", 6)
op_exponentiate = Operator("^", 8, Association.right)
op_negate = Operator("unary-", 7, Association.right, cardinality=1)

# Comparison
op_cmp_equal = Operator("=", 1)
op_cmp_not_equal = Operator("!=", 1)
op_cmp_greater_than_or_equal = Operator(">=", 1)
op_cmp_less_than_or_equal = Operator("<=", 1)
op_cmp_greater_than = Operator(">", 1)
op_cmp_less_than = Operator("<", 1)

# Null
op_null_coalesce = Operator("?", 7)

# Logic
op_logical_not = Operator("unary!", 4, Association.right, cardinality=1)
op_logical_or = Operator("|", 2)
op_logical_and = Operator("&", 3)

operators = [
  op_add,
  op_subtract,
  op_multiply,
  op_divide,
  op_modulus,
  op_exponentiate,
  op_negate,
  op_cmp_equal,
  op_cmp_not_equal,
  op_cmp_greater_than_or_equal,
  op_cmp_less_than_or_equal,
  op_cmp_greater_than,
  op_cmp_less_than,
  op_null_coalesce,
  op_logical_not,
  op_logical_or,
  op_logical_and
]

operator_index = {op.symbol: op for op in operators}
