# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import ctypes
import os
import time

####动态库加载######

def load_cdll(dll_path, *dll_funs):
    os.environ["PATH"] += ';' + os.path.dirname(dll_path)
    dll_handle = ctypes.CDLL(dll_path)
    class DllClass(object):
        pass
    rs = DllClass()
    for f_name, f_arg, f_rs in dll_funs:
        fun = dll_handle.__getattr__(f_name)
        fun.argtypes = f_arg
        fun.restype = f_rs
        rs.__setattr__(f_name, fun)
    return rs

####运行程序######
def run_console(bin_path, args, get_result=False, debug_info=False):
    """
    运行一个控制台程序，读取返回的内容
    """
    debug_info and print('%s %s' % (bin_path, args))
    if get_result:
        return os.popen('%s %s' % (bin_path, args)).read()
    else:
        os.system('%s %s' % (bin_path, args))

####接收命令的主循环######
def main_loop(usage):
    """
    接收命令的主循环
    """
    def print_usage():
        print("*" * 50)
        for i in xrange(len(usage)):
            print(('[' + str(i + 1) + ']').ljust(4), '--  '.rjust(30), usage[i][0], sep='')
        print(('[0]').ljust(4), '--  '.rjust(30), '退出', sep='')
        print("*" * 50)
    ext = False
    while not ext: 
        print_usage()
        command = raw_input(">>")
        command = command.split(' ')
        for cd in command:
            try:
                d = int(cd) - 1
            except:
                continue
            if d >= 0 and d < len(usage):
                usage[d][1]()
            elif d < 0:
                ext = True
                break

####打印函数运行时间######
def profile_func(func):
    """
    对函数进行运行时间记录
    用法：调用此函数生新函数，此函数返回原函数的运行结果，和运行时间
    """
    def newFunc(*args, **args2):
        t0 = time.time()
        log_str = "@%s, {%s} start\n" % (time.strftime("%X", time.localtime()), func.__name__)
        print(log_str)
        back = func(*args, **args2)
        log_str = "@%s, {%s} end\n" % (time.strftime("%X", time.localtime()), func.__name__)
        t = time.time() - t0
        print(log_str)
        log_str = "#%.3fs taken for {%s}\n" % (time.time() - t0, func.__name__)
        print(log_str)
        return (back, t)
    return newFunc


if __name__ == '__main__':
    pass
