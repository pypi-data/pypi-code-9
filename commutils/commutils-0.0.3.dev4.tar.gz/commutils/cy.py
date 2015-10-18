#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from __future__ import print_function
from commutils.cli import register_maker,run, subprocess_run,subprocess_shell,wrapper_decorator,autokwoargs
from commutils.project_gen import new_project,update_project
import functools
import commutils.yml_config as config
from commutils.gy import commit,push

import os
import re
import inspect,importlib
from jinja2 import Template

register,_functions=register_maker()


## register放在最后, 这样才能被clize访问到最终的函数


@register
def cd(name=''):
    # os.chdir(name)
    # subprocess_shell('cd \"%s\";open .'%name)
    subprocess_run('cd %s'%name)



def main():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    python shell command and folder shortcut
    """
    # todo: 改进: 按字典键排序生成值的列表.
    commands=_functions
    run(commands,description=description)

# todo: 模板,

if __name__ == '__main__':
    main()


