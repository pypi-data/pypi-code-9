#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import shell_task

class TestShell_task(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_sccvpn(self):
        return
        shell_task.sccvpn()


    def test_hello_world(self):
        return
        shell_task.hello_world(name=None, no_capitalize=False)


    def test_version(self):
        return
        shell_task.version()


    def test_add(self):
        return
        shell_task.add(*text)


    def test_list(self):
        return
        shell_task.list()


    def test_subprocess_example(self):
        return
        shell_task.subprocess_example()


    def test_sh_example(self):
        return
        shell_task.sh_example()


    def test_wrapper_example(self):
        return
        shell_task.wrapper_example()


    def test_with_uppercase(self):
        return
        shell_task.with_uppercase(wrapped,uppercase=False, *args, **kwargs)


    def test_hello_world(self):
        return
        shell_task.hello_world(name=None)


    def test_decorator_example(self):
        return
        shell_task.decorator_example()


    def test_with_uppercase2(self):
        return
        shell_task.with_uppercase2(aaa,bbb=0)


    def test_n(self):
        return
        shell_task.n(wrapped)


    def test_new(self):
        return
        shell_task.new(*args)


    def test_hello_world2(self):
        return
        shell_task.hello_world2(name=None)


    def test_destruct_example(self):
        return
        shell_task.destruct_example()


    def test_func(self):
        return
        shell_task.func(x,y)



if __name__ == '__main__':
    unittest.main()



