def print_lol(the_list, indent=false, level=0):
	for i in the_list:
		if isinstance(i,list):
			print_lol(i, indent, level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			else:
				print(i)