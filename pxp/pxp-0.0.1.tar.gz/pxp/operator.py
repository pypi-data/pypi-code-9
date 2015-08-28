from pyebnf.operator import Association, Operator


# Arithmetic
op_add = Operator("+", 6)
op_subtract = Operator("-", 6)
op_multiply = Operator("*", 7)
op_divide = Operator("/", 7)
op_modulus = Operator("%", 7)
op_exponentiate = Operator("^", 8, Association.right)

# Comparison
op_cmp_equal = Operator("=", 1)
op_cmp_not_equal = Operator("!=", 1)
op_cmp_greater_than_or_equal = Operator(">=", 1)
op_cmp_less_than_or_equal = Operator("<=", 1)
op_cmp_greater_than = Operator(">", 1)
op_cmp_less_than = Operator("<", 1)

# Null
op_null_coalesce = Operator("?", 2)

# Logic
op_logical_not = Operator("!", 5, Association.right, cardinality=1)
op_logical_or = Operator("|", 3)
op_logical_and = Operator("&", 4)

operators = [
  op_add,
  op_subtract,
  op_multiply,
  op_divide,
  op_modulus,
  op_exponentiate,
  op_cmp_equal,
  op_cmp_not_equal,
  op_cmp_greater_than_or_equal,
  op_cmp_less_than_or_equal,
  op_cmp_greater_than,
  op_cmp_less_than,
  op_logical_not,
  op_logical_or,
  op_logical_and
]

operator_index = {op.symbol: op for op in operators}
