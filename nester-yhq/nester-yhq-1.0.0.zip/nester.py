"""这是"nester.py"模块，提供了一个名为fun()的函数"""
def fun(item):
    """该函数的作用是打印数据项或列表，其中有可能包含嵌套列表"""
    if isinstance(item, list):
        for each in item:
            fun(each)
    else :
        print(item)

        
    
