def Print(the_list,level=0):
	for each  in the_list:
		if isinstance(each,list):
			Print(each,level+1)
		else:
			for tab_num in range(level):
				print("\t", end='')
			print(each)


