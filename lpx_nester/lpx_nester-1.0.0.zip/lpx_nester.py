'''aaaaaa aaaaaa'''
def print_lol(the_item):      
	for each_item in the_item:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
 
