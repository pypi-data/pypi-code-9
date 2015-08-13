#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About
~~~~~

**Copyright (c) 2015 by Sanhe Hu**

- Author: Sanhe Hu
- Email: husanhe@gmail.com
- Lisence: MIT


**Compatibility**

- Python2: Yes
- Python3: Yes
    

**Prerequisites**

- None

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function, unicode_literals
            
class Messenger():
    """An utility class to easily disable or enable all your print function.

    Sometime you may have a lots of print("something") in your script. But how 
    about if you want to disable them all or part of them? Usually we have to 
    comment them all. But Messenger provide Messenger.off() and Messenger.on() 
    to easily trigger On/Off all Messenger.show() functionality.
        
    Usage:
    
    1. use Messenger.show("something") to replace all your print("something")
        
    2. call ``Messenger.off()`` to disable all Messenger.show()
        
    3. call ``Messenger.on()`` to enable all Messenger.show()
            
    ------
    
    **中文文档**
    
    在python程序中为了调试方便, 我们通常会有大量的print()。但是如果我们想要一次
    性禁用大量的print(), 我们就需要很麻烦的注释掉许多print()。Messenger提供了
    一种解决方案能在修改极少的代码的情况下, 解决这一问题。
    
    1. 每当我们想要用print()的时候, 我们可以使用Messenger.show("something")。
    2. 但是我们想要一次性禁用之后所有的print(), 我们只需要调用Messenger.off()。
    3. 同样如果需要恢复打印功能, 我们只需要调用Messenger.on()即可。
    """
    def __init__(self, enable_verbose=True):
        """echo=False to disable all Messenger.show()
        """
        self.enable_verbose = enable_verbose
        if self.enable_verbose:
            self.show = self._print_screen
        else:
            self.show = self._not_print_screen
            
    def _print_screen(self, text):
        print(text)
        
    def _not_print_screen(self, text):
        pass

    def on(self):
        """enable Messenger.show()"""
        self.show = self._print_screen
        
    def off(self):
        """disable Messenger.show()"""
        self.show = self._not_print_screen

messenger = Messenger()

if __name__ == "__main__":
    """only print 1, 4 and 5.
    """
    messenger.show("1")
    messenger.off()
    messenger.show("2")
    messenger.show("3")
    messenger.on()
    messenger.show("4")
    messenger.show("5")