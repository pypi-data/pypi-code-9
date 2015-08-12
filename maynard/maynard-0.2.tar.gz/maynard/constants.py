import __future__
import dis
import sys
import opcode

from inspect import CO_OPTIMIZED, CO_NEWLOCALS, CO_VARARGS
from inspect import CO_VARKEYWORDS, CO_NESTED, CO_GENERATOR, CO_NOFREE

# these flags aren't exported, but you can still access them with a dot, so...
CO_NESTED = __future__.CO_NESTED
CO_GENERATOR_ALLOWED = __future__.CO_GENERATOR_ALLOWED
CO_FUTURE_DIVISION = __future__.CO_FUTURE_DIVISION
CO_FUTURE_ABSOLUTE_IMPORT = __future__.CO_FUTURE_ABSOLUTE_IMPORT
CO_FUTURE_WITH_STATEMENT = __future__.CO_FUTURE_WITH_STATEMENT
CO_FUTURE_PRINT_FUNCTION = __future__.CO_FUTURE_PRINT_FUNCTION
CO_FUTURE_UNICODE_LITERALS = __future__.CO_FUTURE_UNICODE_LITERALS
CO_FUTURE_BARRY_AS_BDFL = __future__.CO_FUTURE_BARRY_AS_BDFL


Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE, \
PyCmp_IN, PyCmp_NOT_IN, PyCmp_IS, \
PyCmp_IS_NOT, PyCmp_EXC_MATCH, PyCmp_BAD = range(12)


base_opcodes = {}
reverse_base_opcodes = {}

op_max_length = -1
for name, op in dis.opmap.items():
	name = name.lower()
	base_opcodes[name] = op
	reverse_base_opcodes[op] = name
	op_max_length = max(len(name), op_max_length)

argument_threshold = dis.HAVE_ARGUMENT

version = float(str(sys.version_info.major) + "." + str(sys.version_info.minor))

def get_op(name, first=0, last=100):
	op = base_opcodes.get(name, -1)
	# print("get_op", name.ljust(28), str(op).ljust(4), str(version).ljust(4), str(first).ljust(4), str(last).ljust(4))
	if version < first or version > last:
		assert op == -1
	else:
		assert op >= 0
	return op


op_before_async_with          = get_op("before_async_with", 3.5)
op_binary_add                 = get_op("binary_add")
op_binary_and                 = get_op("binary_and")
op_binary_floor_divide        = get_op("binary_floor_divide")
op_binary_lshift              = get_op("binary_lshift")
op_binary_modulo              = get_op("binary_modulo")
op_binary_matrix_multiply     = get_op("binary_matrix_multiply", 3.5)
op_binary_multiply            = get_op("binary_multiply")
op_binary_or                  = get_op("binary_or")
op_binary_power               = get_op("binary_power")
op_binary_rshift              = get_op("binary_rshift")
op_binary_subscr              = get_op("binary_subscr")
op_binary_subtract            = get_op("binary_subtract")
op_binary_true_divide         = get_op("binary_true_divide")
op_binary_xor                 = get_op("binary_xor")
op_break_loop                 = get_op("break_loop")
op_build_list                 = get_op("build_list")
op_build_list_unpack          = get_op("build_list_unpack", 3.5)
op_build_map                  = get_op("build_map")
op_build_map_unpack           = get_op("build_map_unpack", 3.5)
op_build_map_unpack_with_call = get_op("build_map_unpack_with_call", 3.5)
op_build_set                  = get_op("build_set")
op_build_set_unpack           = get_op("build_set_unpack", 3.5)
op_build_slice                = get_op("build_slice")
op_build_tuple                = get_op("build_tuple")
op_build_tuple_unpack         = get_op("build_tuple_unpack", 3.5)
op_call_function              = get_op("call_function")
op_call_function_kw           = get_op("call_function_kw")
op_call_function_var          = get_op("call_function_var")
op_call_function_var_kw       = get_op("call_function_var_kw")
op_compare_op                 = get_op("compare_op")
op_continue_loop              = get_op("continue_loop")
op_delete_attr                = get_op("delete_attr")
op_delete_deref               = get_op("delete_deref", 3.2)
op_delete_fast                = get_op("delete_fast")
op_delete_global              = get_op("delete_global")
op_delete_name                = get_op("delete_name")
op_delete_subscr              = get_op("delete_subscr")
op_dup_top                    = get_op("dup_top")
op_dup_top_two                = get_op("dup_top_two", 3.2)
op_dup_top                    = get_op("dup_top_x", 0, 3.1)
op_end_finally                = get_op("end_finally")
op_extended_arg               = get_op("extended_arg")
op_for_iter                   = get_op("for_iter")
op_get_aiter                  = get_op("get_aiter", 3.5)
op_get_anext                  = get_op("get_anext", 3.5)
op_get_awaitable              = get_op("get_awaitable", 3.5)
op_get_iter                   = get_op("get_iter")
op_get_yield_from_iter        = get_op("get_yield_from_iter", 3.5)
op_import_from                = get_op("import_from")
op_import_name                = get_op("import_name")
op_import_star                = get_op("import_star")
op_inplace_add                = get_op("inplace_add")
op_inplace_and                = get_op("inplace_and")
op_inplace_floor_divide       = get_op("inplace_floor_divide")
op_inplace_lshift             = get_op("inplace_lshift")
op_inplace_modulo             = get_op("inplace_modulo")
op_inplace_matrix_multiply    = get_op("inplace_matrix_multiply", 3.5)
op_inplace_multiply           = get_op("inplace_multiply")
op_inplace_or                 = get_op("inplace_or")
op_inplace_power              = get_op("inplace_power")
op_inplace_rshift             = get_op("inplace_rshift")
op_inplace_subtract           = get_op("inplace_subtract")
op_inplace_true_divide        = get_op("inplace_true_divide")
op_inplace_xor                = get_op("inplace_xor")
op_jump_absolute              = get_op("jump_absolute")
op_jump_forward               = get_op("jump_forward")
op_jump_if_false_or_pop       = get_op("jump_if_false_or_pop")
op_jump_if_true_or_pop        = get_op("jump_if_true_or_pop")
op_list_append                = get_op("list_append")
op_load_attr                  = get_op("load_attr")
op_load_build_class           = get_op("load_build_class")
op_load_classderef            = get_op("load_classderef", 3.4)
op_load_closure               = get_op("load_closure")
op_load_const                 = get_op("load_const")
op_load_deref                 = get_op("load_deref")
op_load_fast                  = get_op("load_fast")
op_load_global                = get_op("load_global")
op_load_name                  = get_op("load_name")
op_make_closure               = get_op("make_closure")
op_make_function              = get_op("make_function")
op_map_add                    = get_op("map_add")
op_nop                        = get_op("nop")
op_pop_block                  = get_op("pop_block")
op_pop_except                 = get_op("pop_except")
op_pop_jump_if_false          = get_op("pop_jump_if_false")
op_pop_jump_if_true           = get_op("pop_jump_if_true")
op_pop_top                    = get_op("pop_top")
op_print_expr                 = get_op("print_expr")
op_raise_varargs              = get_op("raise_varargs")
op_return_value               = get_op("return_value")
op_rot_three                  = get_op("rot_three")
op_rot_two                    = get_op("rot_two")
op_rot_four                   = get_op("rot_four", 0, 3.1)
op_set_add                    = get_op("set_add")
op_setup_async_with           = get_op("setup_async_with", 3.5)
op_setup_except               = get_op("setup_except")
op_setup_finally              = get_op("setup_finally")
op_setup_loop                 = get_op("setup_loop")
op_setup_with                 = get_op("setup_with", 3.2)
op_stop_code                  = get_op("stop_code", 0, 3.2)
op_store_attr                 = get_op("store_attr")
op_store_deref                = get_op("store_deref")
op_store_fast                 = get_op("store_fast")
op_store_global               = get_op("store_global")
op_store_locals               = get_op("store_locals", 0, 3.3)
op_store_map                  = get_op("store_map", 0, 3.4)
op_store_name                 = get_op("store_name")
op_store_subscr               = get_op("store_subscr")
op_unary_invert               = get_op("unary_invert")
op_unary_negative             = get_op("unary_negative")
op_unary_not                  = get_op("unary_not")
op_unary_positive             = get_op("unary_positive")
op_unpack_ex                  = get_op("unpack_ex")
op_unpack_sequence            = get_op("unpack_sequence")
op_with_cleanup               = get_op("with_cleanup", 0, 3.4)
op_with_cleanup_start         = get_op("with_cleanup_start", 3.5)
op_with_cleanup_finish        = get_op("with_cleanup_finish", 3.5)
op_yield_from                 = get_op("yield_from", 3.3)
op_yield_value                = get_op("yield_value")


def opcode_set(opcodes):
	values = set()
	for s in opcodes.strip().split():
		values.add(base_opcodes[s])
	return values

absolute_jumps = opcode_set("""
	jump_if_false_or_pop
	jump_if_true_or_pop
	jump_absolute
	pop_jump_if_false
	pop_jump_if_true
	""")

relative_jumps = opcode_set("""
	for_iter
	jump_forward
	""")

all_jumps = absolute_jumps | relative_jumps


all_names = opcode_set("""
	delete_attr
	delete_global
	load_attr
	load_global
	store_attr
	store_global
	""")

all_locals = opcode_set("""
	delete_fast
	load_fast
	store_fast
	""")

all_consts = opcode_set("""
	load_const
	""")

if ((sys.version_info.major > 3) or
	(sys.version_info.major == 3 and sys.version_info.minor >= 4)):
	def stack_effect(op, oparg):
		try:
			return opcode.stack_effect(op, oparg)
		except ValueError:
			pass
		raise ValueError("invalid opcode or oparg: " + str(op) + " " + str(oparg))
else:

	from .stackeffect import *

	if __name__ == "__main__":
		# check that all opcodes whose stack effect
		# change with the oparg actually do
		negative_nine = opcode_set("""
				build_list
				build_set
				build_slice
				build_tuple
				call_function
				call_function_kw
				call_function_var
				call_function_var_kw
				make_closure
				make_function
				raise_varargs
				unpack_ex
				unpack_sequence
				""")

		for op in range(256):
			value = opcode_stack_effect[op]
			is_special = value == -9
			should_be_special = op in negative_nine
			if is_special:
				assert should_be_special, "fail op "+ str(op)
			else:
				assert not should_be_special, "fail op "+ str(op)

	def stack_effect(op, argument):
		effect = opcode_stack_effect[op]
		if effect is None:
			raise ValueError("invalid opcode or oparg: " + str(opcode) + " " + str(oparg))
		if effect != -9:
			return effect
		assert argument != None

		if op == op_unpack_sequence:
			return argument - 1
		if op == op_unpack_ex:
			return (argument & 0xFF) + (argument >> 8)
		if op in (op_build_tuple, op_build_list, op_build_set):
			return 1 - argument;
		if op == op_raise_varargs:
			return -argument;
		if op == op_build_slice:
			if (oparg == 3):
				return -2
			return -1

		def nargs(o): return (((o) % 256) + 2*(((o) // 256) % 256))

		if op == op_call_function:
			return -nargs(argument)
		if op in (op_call_function_var, op_call_function_kw):
			return -nargs(argument) - 1
		if op == op_call_function_var_kw:
			return -nargs(argument) - 2
		if op == op_make_function:
			return -1 - nargs(argument) - ((argument >> 16) & 0xffff)
		if op == op_make_closure:
			return -2 - nargs(argument) - ((argument >> 16) & 0xffff)
		assert False, "shouldn't get here"
