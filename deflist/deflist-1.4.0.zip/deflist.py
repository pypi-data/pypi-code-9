"""
在原有功能基础上，增加打印时没出现一层嵌套就缩进显示一个TAB制表符(增加了一个新的参数level(0，1，2))
为了使模块功能变的更为灵活，把模块中必备的两个参数中的一个改为可选参数为它添加缺省值
the last modify,为函数增加第三个参数(indent)，开始时这个参数值设置为False，也就是说默认情况下不打开缩进特性，当参数值为True时，显示缩进特性
"""
"""
给print_list函数增加第4个参数，用来标识将把数据写入那个位置，一定要为这个参数提供缺省值sys.stdout，这样如果调用这个函数时没有指定文件对象则会依然写至屏幕；

"""
def print_list(the_list,indent=False,level=0,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item,indent,level+1,fh) #每打印一次参数+1,表示下次打印列表时多增加一个TAB制表符
        else:
             if indent:
                for tab_stop in range(level):
                      print("\t",end=" ",file=fh)#调整两个“print()”,调用来使用这个新参数
            print(each_item,file=fh)
