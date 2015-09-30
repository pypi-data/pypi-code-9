def Print(the_list,indent=False,level=0):
	for each  in the_list:
		if isinstance(each,list):
			Print(each,indent,level+1)
		else:
			if indent:
				for tab_num in range(level):
					print("\t",*level, end='')
			print(each)


