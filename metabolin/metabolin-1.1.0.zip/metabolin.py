"""
	select every item from a list and print.
"""

def print_lol(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)
			
			
# END