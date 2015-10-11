def print_loo(the_list):
	for ea in the_list:
		if isinstance(ea,list):
			print_loo(ea)
		else:
			print(ea)