"""This is the nester.py module, it contains the rep() function 
that prints lists that may or may not contain nested lists"""
def rep(movies):
        #Reccursive function, prints each primitive
         #  element in a new line, breaking down nested lists""" 
	for each_flic in movies:
		if isinstance(each_flic,list):
			rep(each_flic)
		else:
			print(each_flic)
