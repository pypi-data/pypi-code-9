#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from __future__ import print_function
from commutils.cli import (
    register_maker,run, subprocess_run,subprocess_shell,
    wrapper_decorator,autokwoargs,cd
)
from commutils.project_gen import new_project,update_project
import functools
import commutils.yml_config as config
from commutils.gy import commit,push

import os
import re
import inspect,importlib
from jinja2 import Template

register,_functions=register_maker()


def check_setup_py_origin(f):
    ## 保持原函数的__doc__和__name__

    @functools.wraps(f)
    @autokwoargs
    # 这里不能用*args, **kwargs, 因为clize不支持这样的函数头部.
    def wrapper(*args, **kwargs):
        print ('=============================')
        print (os.path.abspath('.'))
        print(os.path.exists('setup.py'))
        if not os.path.exists('setup.py'):
            print('ERROR: setup.py do not exist. Please check your path.')
            exit(0)
        else:
            return f(*args,**kwargs)
    return wrapper

## 用这个版本可以和clize一起正确处理*args, **kwargs, 另外函数不一定要return.
@wrapper_decorator
def check_setup_py(f,*args,**kwargs):
    if not os.path.exists('setup.py'):
        print('ERROR: setup.py do not exist. Please check your path.')
    else:
        return f(*args,**kwargs)


## register放在最后, 这样才能被clize访问到最终的函数
@register
@check_setup_py
def build():
    '''
    hello
    :return:
    '''
    clean_build()
    command='python setup.py sdist'
    subprocess_run(command)

@register
@check_setup_py
def install():
    clean_build()
    command='python setup.py install --record install.txt'
    subprocess_run(command)

@register
@check_setup_py
def install_locally():
    clean_build()
    command='python setup.py install --prefix=~/.local --record install.txt'
    subprocess_run(command)

@register
@check_setup_py
def uninstall():
    command='rm -rf `cat install.txt`'
    subprocess_shell(command)

@register
@check_setup_py
@autokwoargs
def upload(test=False):
    if test:
        command='python setup.py register -r testpypi'
        subprocess_run(command)
        command='python setup.py sdist upload -r testpypi '
        subprocess_run(command)
    else:
        command='python setup.py register -r pypi'
        subprocess_run(command)
        command='python setup.py sdist upload -r pypi '
        subprocess_run(command)



@register
@check_setup_py
@autokwoargs
def pip_install(test=False):
    command="pip install -i https://pypi.python.org/pypi commutils --user --upgrade"
    subprocess_run(command)

@register
@check_setup_py
@autokwoargs
def detox(r=False):
    if not r:
        command='detox'
    else:
        command='detox -r'
    subprocess_run(command)


# todo: 学习记录

@register
@check_setup_py
def init_test():
    # todo: bugfix 处理文件夹加__init__.py的形式.


    config.check_config('config.yml')
    package_dir=config.project['name']

    # package_dir="commutils"
    unit_test_dir=os.path.join(package_dir,"tests/unit")

    exclude_dir=set(['tests','target','template','__pycache__'])
    py_pattern=re.compile(r'^(?!__init__).*\.py$')
    replace_pattern=re.compile(r'^%s'%package_dir)
    for root,dirs,files in os.walk(package_dir,topdown=True):
        # 本地修改, 另外列表生成式里面的变量不是局域的, 在用完后会保留.
        dirs[:] = [d for d in dirs if d not in exclude_dir]
        files[:] = [f for f in files if py_pattern.match(f)]
        # print(root,dirs,files)
        for file in files:
            py_file=os.path.join(root,file)
            # test_file=os.path.join(root.replace(package_dir,unit_test_dir),'test_'+file)
            test_root=re.sub(replace_pattern,package_dir+"/tests/unit",root)
            test_file=os.path.join(test_root,'test_'+file)
            # print (test_file)
            if not os.path.exists(test_file):
                module=py_file.replace('.py','')
                module=module.replace('/','.')
                module_path=root.replace('/','.')
                module_name=file.replace('.py','')

                # done: 直接从文件内容里面提取函数名和函数头部
                # all_functions=[(func_name,func_definition),]

                definition_pattern=re.compile(r'^\s*def\s+((.*?)\(.*\))\s*:\s*$',re.M)
                with open(py_file) as f:
                    content=f.read()
                all_functions=definition_pattern.findall(content)
                all_functions=[(j,i) for (i,j) in all_functions]

                # 使用import module & inspect 的方法获取func_name和func_definition
                # imported_module=importlib.import_module(module)
                # all_functions = inspect.getmembers(imported_module, inspect.isfunction)
                # definition_pattern=re.compile(r'def (.*):')
                # all_functions=[(i[0],definition_pattern.search(inspect.getsource(i[1])).group(1)) for i in all_functions]



                if not os.path.exists(test_root):
                    os.makedirs(test_root)

                with open(os.path.join('template_test.pytemplate')) as f:
                    content=Template(f.read()).render(module_path=module_path,module_name=module_name,all_functions=all_functions)
                # print content

                with open(test_file,'w') as f:
                    f.write(content)

# project_gen=register(project_gen)
@register
def new(name='new'):
    new_project(name)
    # print(os.path.abspath('.'))


@register
@check_setup_py
def project_update():
    update_project()
    # print(os.path.abspath('.'))

@check_setup_py
def clean_build():
    subprocess_run('rm -rf build')



@register
def self_update():
    current=os.path.abspath('.')
    with cd("/Users/lhr/_action/python/projects/commutils"):
        commit()
        clean_build()
        # subprocess_run("commutils/ly.py install")
        install()


@register
def publish():
    push()
    build()  # build只生成dist目录的压缩包
    upload() # 生成压缩包并上传
    self_update() # 用本地的代码直接build到build目录, 然后安装

# @register
# def local_publish():
#     commit()
#     build()
#     self_update()

def main():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    python project manager
    """
    # todo: 改进: 按字典键排序生成值的列表.
    commands=_functions
    run(commands,description=description)

# todo: 模板,

if __name__ == '__main__':
    main()


