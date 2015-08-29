"""This is the "innerPrinter.py" module, including a function
(innerListPrinter()), which prints list-items individually,
even if the items are lists themselves"""

def innerListPrinter(the_list, level = 0):
	"""The function takes two arguments called "the_list" and "level".
		It prints each data item in the list on its own line recursively.
		Passing a number k in the second argument(or nothing), the items will be printed
		k TAB-times more right when they are in nested list. """
	for item in the_list:
		if isinstance(item, list):
			innerListPrinter(item, level + 1)
		else:
			for tab in range(level):
				print("\t", end = "")
			print(item)