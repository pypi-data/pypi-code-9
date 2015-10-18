#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
# subprocess: https://docs.python.org/2.6/library/subprocess.html
# sh: https://amoffat.github.io/sh/#interactive-callbacks
# clize: http://clize.readthedocs.org/en/3.0/why.html


from __future__ import print_function
import os,subprocess, sh
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# todo: 解决python3和doc的问题. python3对中文的支持好. macro写好. rest, eve, 启动服务控制.

# from Queue import Queue
from sigtools.modifiers import autokwoargs,kwoargs
from sigtools.wrappers import wrapper_decorator
from clize import run


## =====================
## 正式任务

def sccvpn():
    '''
    connect to ustc scc vpn, the config file's location is /Users/lhr/_env/vpn/ustc_scc_vpn/

    '''
    origin_path=os.path.curdir
    os.chdir("/Users/lhr/_env/vpn/ustc_scc_vpn/")
    # sh.sudo.openvpn('--config','./ustc-scc.ovpn') # this not works! sh会拦截stdin
    subprocess.call(['sudo','openvpn','--config','./ustc-scc.ovpn'])
    os.chdir(origin_path)






### 测试clize
@kwoargs('no_capitalize')
def hello_world(name=None, no_capitalize=False):
    """Greets the world or the given name.

    name: If specified, only greet this person.

    no_capitalize: Don't capitalize the given name.
    """
    if name:
        if not no_capitalize:
            name = name.title()
        print('Hello {0}!'.format(name))
        return
    print('Hello world!')
    return

VERSION=1.0
def version():
    """Show the version"""
    return '{0} version {1}'.format(__file__,VERSION)

def add(*text):
    """Adds an entry to the to-do list.

    text: The text associated with the entry.
    """
    return "OK I will remember that."


def list():
    """Lists the existing entries."""
    return "Sorry I forgot it all :("

if __name__ == '__main__':

    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    A reliable to-do list utility.

    Store entries at your own risk.
    """

    run([hello_world,list,sccvpn,version],description=description)
    # run(hello_world,alt=[version])












## subprocess和sh的example
def subprocess_example():
    # subprocess 用法, 默认不拦截stdio. https://docs.python.org/2.6/library/subprocess.html
    # p=subprocess.Popen(['cat']) # 如果是Popen则先挂起了, 直到communicate才激活输入输出
    # p=subprocess.call(['cat'])  # 要用call或者check_call, call失败时返回返回码, check_call失败时候返回异常
    # 要拦截的话就用surprocess.PIPE
    p=subprocess.Popen(['cat'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # 然后用communicate 传入输入, 获得输出, 阻塞, 因为没有回调函数.
    output=p.communicate(input="good")[0]
    print(output)
    # subprocess接收的是分离的参数列表数组. 可以用shlex解析字符串得到.
    # >>> import shlex, subprocess
    # >>> command_line = raw_input()
    # /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
    # >>> args = shlex.split(command_line)
    # >>> print args
    # ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
    # >>> p = subprocess.Popen(args) # Success!
def sh_example():
    # sh文档, https://amoffat.github.io/sh/#interactive-callbacks
    def process_output(line, stdin, process): # 第一个参数是输出的内容. stdin标准输入, process进程
        print(line)
        if "ERROR" in line:
            process.terminate()
            return True
    # Warnning!!! 1.sh会在等待用户输入处卡住. 2.如果命令执行失败会异常.
    # sh用法: 默认拦截stdio. 一定要注意测试通过, 不要被stdio卡住, 参考sh文档的最后关于tty的说明 可以试着抛出异常?.
    s="good"
    # 用_in传入string, 或者数组
    p=sh.cat(_in=s)
    print (p)
    # 用_out传出文件, StringIO, 或文件名
    output=StringIO()  # StringIO有write()方法, 也可以用print>>追加内容, get_value()方法相当于read, close()关闭
    p=sh.cat(_in=s,_out=output)
    # 用StringIO类型的output变量捕获sh的输出, 注意要用get_value()把内容读出.
    print (output.getvalue())
    # 可以传入回调函数处理out输出的内容, 所以是异步的.
    p=sh.cat(_in=s,_out=process_output)

    # 还有一个可以处理stdin的管道用法, 以后参阅https://amoffat.github.io/sh/#interactive-callbacks
    # q=Queue()
    # q.put("good2")
    # p=sh.cat(_in=q,_out=process_output)

    # def interact(line, stdin):
    #     print line
    #     if line == "What... is the air-speed velocity of an unladen swallow?":
    #         stdin.put("What do you mean? An African or European swallow?")
    #
    #     elif line == "Huh? I... I don't know that....AAAAGHHHHHH":
    #         cross_bridge()
    #         return True
    #
    #     else:
    #         stdin.put("I don't know....AAGGHHHHH")
    #         return True
    # p = tail(_tty_in=True,_out="out.log")
    # p.wait()
    # print p
def wrapper_example():
    '''
    wrapper_decorator: 把当前函数变成一个装饰wrapper函数的装饰器. 原理需要构造一个返回装饰器的函数.
    autokwoargs: 自动把关键字参数变成关键字而不受调用参数顺序的影响, 相当于自动把关键字放到参数的末尾.
    wrapper_decorator和autokwoargs要联合起来用, 结合*args, **kwargs传递原函数的参数. 是固定用法. /这样才能传递原函数的所有参数. 如果想自由组合参数, 也可以专门调整.
    因为没有宏, 所以这些模式要记住, 固定使用. 如果有宏则可以把这些用宏写成更简单的包裹(或者说抽象).
    '''
    @wrapper_decorator
    @autokwoargs
    def with_uppercase(wrapped,uppercase=False, *args, **kwargs):
        """
        Formatting options:

        uppercase: Print output in capitals
        """
        ret = wrapped(*args, **kwargs)
        if uppercase:
            return str(ret).upper()
        else:
            return ret


    @with_uppercase
    def hello_world(name=None):
        """Says hello world

        name: Who to say hello to
        """
        if name is not None:
            return 'Hello ' + name
        else:
            return 'Hello world!'

    print (hello_world("good", uppercase=True)) # 这里必须用关键字调用, 因为其余参数都会为hello_world原参数

    # 附录: 自己实现的一个wrapper_decorator, 但是介于python decorator的格式, 内部返回decorator好像不行. 以下并不能正确.
    # def wrapper_decorator2(func):
    #     def newfunc(wrapper,*args,**kwargs):
    #         def decorator(wrapper):
    #             def decratored(*args, **kwargs):
    #                 return func(wrapper,*args,**kwargs)
    #
    #                 # return wrapper(*args, **kwargs)
    #             return decratored
    #         return decorator
    #     return newfunc
def decorator_example():
    '''
    装饰器的用法, 装饰器第一个参数是被装饰的函数, 如果装饰器带参数要再包裹一层.
    之后就是返回一个修饰过的函数. 最内层的函数就是修饰的过程, 有新的参数列表, 可以调用传入的函数名(应用参数列表), 装饰器参数等
    闭包相当于用变量配置一个函数. 装饰器相当于用函数配置一个函数, 把函数传到闭包里面.
    '''
    def with_uppercase2(aaa,bbb=0):
        def n(wrapped):
            def new(*args):
                print(aaa,bbb)
                print(*args)
                # *args 列表收集, 解构的反义词, *本身就是解构.
                print(wrapped(*args))
                return wrapped(*args)
            return new
        return n

    @with_uppercase2("aaa")
    def hello_world2(name=None):
        """Says hello world

        name: Who to say hello to
        """
        if name is not None:
            return 'Hello ' + name
        else:
            return 'Hello world!'

    print ( hello_world2("good"))
def destruct_example():
    ''' *args 列表收集, 解构的反义词, *本身就是解构.'''
    def func(x,y):
        print( x,y)
    a=[1,2]
    func(*a)
    func(*[2,4])
