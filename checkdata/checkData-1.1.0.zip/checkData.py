# _*_ coding: utf-8 _*_
#循环迭代列表的小程序

""" program for check list """
def checkData(to_do_list,level):
	for list_item in to_do_list:
		if isinstance(list_item,list):
			checkData(list_item,level+1)
		else:
                        for num in range(level):
                                print ("\t",end = '')
			print (list_item)
