def print_lol(element):
	for y in element:
		if isinstance(y,list):
				return print_lol(y)
		else:
			print(y)