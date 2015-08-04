def print_AOL(the_list):
	for movie in the_list:
		if isinstance(movie,list):
			print_AOL(movie)
		else:
			print (movie)

def print_AOL(the_list,num):
	for item in the_list:
		if isinstance(item,list):
			print_AOL(item,num)
		else:
			for tab_stop in range(num):
				print("\t",end='')
			print(item)
