def print_movies(spaceStr, the_list):
    for each_movie in the_list:
        if isinstance(each_movie, list):
            print_movies(spaceStr + "    ", each_movie)
        else:
            print(spaceStr + each_movie)
