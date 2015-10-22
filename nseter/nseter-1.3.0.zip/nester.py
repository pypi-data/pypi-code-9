__author__ = 'Administrator'
#coding=utf-8
"""这是‘nester.py'模块，提供了一个名为print_lol的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表"""
def print_lol(the_list,indent=False,level=0):
    """这个函数去一个位置参数，名为"the_list",这可以是任何python列表，列表中的每一项数据被递归的输出到屏幕上，各数据项各占一行"""
    for each_movies in the_list:
        if isinstance(each_movies,list):
            print_lol(each_movies,indent,level+1)
        else:
            if indent:
               for tab_level in range(level):
                    print("\t",end='')
            print(each_movies)