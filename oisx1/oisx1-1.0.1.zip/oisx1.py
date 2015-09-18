def prints(lst, level):
	for it in lst:
		if(isinstance(it, list)):
			prints(it,level+1)
		else:
                        for tabs in range(level):
                                print('\t',end='')
                        print(it)
