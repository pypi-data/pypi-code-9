def Print(the_list):
	for each  in the_list:
		if isinstance(each,list):
			Print(each)
		else:
			print(each)


