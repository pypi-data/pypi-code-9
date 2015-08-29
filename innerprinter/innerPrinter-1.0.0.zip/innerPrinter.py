"""This is the "innerPrinter.py" module, including a function
(innerListPrinter()), which prints list-items individually,
even if the items are lists"""

def innerListPrinter(the_list):
	"""The function takes one argument called "the_list",
	   which is a list. It prints each data item in the list
	   on its own line recursively."""
	for item in the_list:
		if isinstance(item, list):
			innerListPrinter(item)
		else:
			print(item)