def print_all(the_list,level):
    for item in the_list:
        if isinstance(item,list):
            print_all(item,level+1)
        else:
            for i in range(level):
			    print("\t",end='')
			print(item)
