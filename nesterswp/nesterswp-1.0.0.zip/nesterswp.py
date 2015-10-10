""" Function to recursively nest any list """
def p(x):
	for i in x:
		if isinstance(i,list):
			p(i)
		else:
			print (i)
