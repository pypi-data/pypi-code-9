def getNames(list_name,level,indent=false):

	""" 这个函数是一个位置参数，，名为list_name
	这可以使任何Python列表（包含或不包含嵌套列表）
	所提供列表中的各个数据项会（递归的）打印到屏幕上，而且各占一行
	第二个参数（名为‘level’）用来在遇到嵌套列表时插入制表符
	""" 
	for each_name in list_name:
		if isinstance(each_name,list):
			getNames(each_name,level+1,indent)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
				print(each_name)