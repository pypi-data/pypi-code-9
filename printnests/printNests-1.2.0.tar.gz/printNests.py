""" 
This is a comment to describe the print_movie function
which prints the list of movies
movies = ["Inception",2008,"Chris Nolan",126,["De Capri",["Tom Hardy","Dileep Rao","Ken Wantenbe","Ellen Page"]]]
"""

def print_movie(movie_list,feature=False,k=0):
	for movie in movie_list:
		if isinstance(movie,list):
			print_movie(movie,feature,k+1)
		else:
			for space in range(k):
				if feature:
					print("\t",end='')
			print(movie)
