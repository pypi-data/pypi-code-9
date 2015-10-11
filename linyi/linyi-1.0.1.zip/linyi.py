def print_loo(the_list,indent=False,level=0):
	for ea in the_list:
		if isinstance(ea,list):
			print_loo(ea,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(ea)

