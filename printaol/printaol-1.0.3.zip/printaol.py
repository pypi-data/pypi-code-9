def print_AOL(the_list,num = 0):
	for item in the_list:
		if isinstance(item,list):
			print_AOL(item,num+1)
		else:
			for tab_stop in range(num):
				print("\t",end='')
			print(item)
