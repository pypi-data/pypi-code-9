def checkData(this_list,indent=False,level=0):
	for list_item in this_list:
		if isinstance(list_item,list):
			checkData(list_item,indent,level+1)
		else:
			if indent:
				for num in range(level):
					print ("\t",end = '')
			print (list_item)
