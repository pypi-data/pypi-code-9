import time


# for class method checking
def print_running_time(func):
    def wrapper(*arg):
        t = time.clock()
        res = func(*arg)
        print
        print func.func_name + " is running during ", time.clock()-t
        return res
    return wrapper