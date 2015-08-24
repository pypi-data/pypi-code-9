"""This is a nester.py  module. It offers a function to print a list(maybe every element in this list is another list too.) recursive. From book 'Header First Python'"""

def printList(dataList, level):
	"""do iteration."""
	for data in dataList:
		if isinstance(data, list):
			printList(data, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(data)

	#example : print([1,2,3,4])