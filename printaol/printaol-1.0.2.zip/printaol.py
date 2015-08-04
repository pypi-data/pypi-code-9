def print_AOL(the_list,num = 0):
	for item in the_list:
		if isinstance(item,list):
			print_AOL(item,num)
		else:
			for tab_stop in range(num+1):
				print("\t",end='')
			print(item)
