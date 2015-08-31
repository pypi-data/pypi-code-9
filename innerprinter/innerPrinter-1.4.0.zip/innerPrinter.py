"""This is the "innerPrinter.py" module, including a function
(innerListPrinter()), which prints list-items individually,
even if the items are lists themselves"""

import sys

def innerListPrinter(the_list, indent = False, level = 0, printto = sys.stdout):
	"""The function takes two arguments called "the_list" and "level".
		It prints each data item in the list on its own line recursively.
		Passing a number k in the second argument(or nothing), the items will be printed
		k TAB-times more right when they are in nested list. 
		Define the argument printto where you want the list to be printed."""
	for item in the_list:
		if isinstance(item, list):
			innerListPrinter(item, indent, level + 1, printto)
		else:
			if indent:
				for tab in range(level):
					print("\t", end = "", file = printto)
			print(item, file = printto)