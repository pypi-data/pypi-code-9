def print_lol(the_list):
    for each_term in the_list:
        if isinstance(each_term,list):
            return print_lol(each_term)
        else:
            print(each_term)



