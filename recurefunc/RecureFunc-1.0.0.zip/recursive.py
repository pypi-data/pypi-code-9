def print_lol(list_item):
	for each_item in list_item:
		if(isinstance(each_item,list)):
			print_lol(each_item)
		else:
			print(each_item)



