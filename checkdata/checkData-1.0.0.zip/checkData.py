# _*_ coding: utf-8 _*_
#循环迭代列表的小程序

""" program for check list """
def checkData(to_do_list):
	for list_item in to_do_list:
		if isinstance(list_item,list):
			checkData(list_item)
		else:
			print (list_item)
