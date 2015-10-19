# This is the 'nester.py' modele and it provides one function called checklist()
#which print lists that may or may not include nested lists.
def checklist(List):
# This function takes one positional argument called 'List',which is any python
#list (of - possibly - nested lists).Each data item in the provided list is
#(recursively) printed to the screen on it's own line.
	for i in List:
		if isinstance(i,list):
			checklist(i)
		else:
			print(i)
