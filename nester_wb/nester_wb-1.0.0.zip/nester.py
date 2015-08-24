"""This is a nester.py  module. It offers a function to print a list(maybe every element in this list is another list too.) recursive. From book 'Header First Python'"""

def printList(dataList):
	"""do iteration."""
	for data in dataList:
		if isinstance(data, list):
			printList(data)
		else:
			print(data)

	#example : print([1,2,3,4])