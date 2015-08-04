def print_AOL(the_list,indent = False,num = 0):
	for item in the_list:
		if isinstance(item,list):
			print_AOL(item,indent,num+1)
		else:
                        if indent:
                                for tab_stop in range(num):
                                        print("\t",end='')
			print(item)
