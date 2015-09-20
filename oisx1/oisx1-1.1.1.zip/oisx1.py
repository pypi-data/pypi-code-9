def prints(lst, indent=False,level=0):
	for it in lst:
		if(isinstance(it, list)):
			prints(it,indent, level+1)
		else:
			if indent:
				print('\t' * level,end = '')
			print(it)
