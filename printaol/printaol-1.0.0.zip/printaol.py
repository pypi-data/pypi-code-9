def print_AOL(the_list):
	for movie in the_list:
		if isinstance(movie,list):
			print_AOL(movie)
		else:
			print (movie)