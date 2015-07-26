"""This is the "pyso_nester.py" module and it provides one function called print_overly_nested_list()
	which prints lists that may or may not include nested lists."""

def print_deeperlist(the_list):
	"""This function takes one positional argument called "the_list", 
		which is any Python list (of - possibly - nested lists). Each data item in the
		provided list is (recursviely) printed to the screen on it's own line."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_deeperlist(each_item)
		else:
			print each_item		  	