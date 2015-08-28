def print_jx(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_jx(each_item)
		else:
			print(each_item)