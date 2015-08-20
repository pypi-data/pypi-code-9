""" This module holds the commonly used functions """

#This function accepts the list , parse and if the elements in the list is inturn a list the recurssive call is made else element is printed on the console

def parse_list(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			parse_list(each_item)
		else:
			print(each_item)
