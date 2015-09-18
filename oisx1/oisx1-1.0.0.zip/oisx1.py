def prints(lst):
	for it in lst:
		if(isinstance(it, list)):
			prints(it)
		else:
			print(it)