def print_jx(the_list，level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_jx(each_item,level)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)