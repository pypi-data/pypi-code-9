#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from jinja2 import Template
from commutils.cli import (
    subprocess,shlex,os,
    subprocess_run,subprocess_check_run,subprocess_shell,
    register_maker,run,
)

from commutils.reflection import get_script_location
SCRIPT_LOCATION=get_script_location(__file__)
import re
from commutils import yml_config as config

import  six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')


project={
    'name':'new2',
    'author':'lhr',
    'author_email':'airhenry@gmail.com',
    'git_account':'lhrkkk'
}


register,_functions=register_maker()

@register
def project_gen():
    # 拷贝一份并重命名project_name
    subprocess_run("rm -rf target")
    subprocess_run("mkdir target")
    subprocess_run("cp -rf template/project target/")
    subprocess_run("mv target/project/project target/project/%s"%project['name'])
    subprocess_run("mv target/project target/%s"%project['name'])


    # 对于新的拷贝
    project_path = os.path.join("target",project['name'])

    for root,dirs,files in os.walk(project_path):
        # print root,dirs,files, '\n\n'
        for file in files:
            with open(os.path.join(root,file),'r') as f:
                s=Template(f.read()).render(project=project)
            with open(os.path.join(root,file),'w') as f:
                f.write(s)

def cummutils_to_jinja(s):
    name_pattern=re.compile(r'^name\s*=\s*(.*)$',re.M)
    s=re.sub(name_pattern,'name = {{ project[\'name\'] }}',s)

    author_pattern=re.compile(r'^author\s*=\s*(.*)$',re.M)
    s=re.sub(author_pattern,'author = {{ project[\'author\'] }}',s)

    email_pattern=re.compile(r'^author-email\s*=\s*(.*)$',re.M)
    s=re.sub(email_pattern,'author-email = {{ project[\'author_email\'] }}',s)

    home_page_pattern=re.compile(r'^home-page\s*=\s*(.*)$',re.M)
    s=re.sub(home_page_pattern,'home-page = https://github.com/{{ project[\'git_account\'] }}/{{ project[\'name\'] }}.git',s)

    name_pattern=re.compile(r'(^packages\s*=(?:\s*|\n*\s+)).*?(\s*\n+\S)',re.S|re.M)
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)
    script_pattern=re.compile(r'(^scripts\s*=(?:\s*|\n*\s+)).*?(\s*\n+\S)',re.S|re.M)
    s=re.sub(script_pattern,'\\1\\2',s)

    name_pattern=re.compile(r'(OS_TEST_PATH\s*=\s*).*?(/tests/unit)')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)

    name_pattern=re.compile(r'(OS_TEST_PATH\s*=\s*).*?(/tests)')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)

    name_pattern=re.compile(r'(bash -c \"find ).*?( -type f -regex)')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)

    name_pattern=re.compile(r'(^source\s*=\s*).*?(\n)')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)

    name_pattern=re.compile(r'(^omit\s*=\s*).*?(/test/)')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)

    name_pattern=re.compile(r'(OS_TEST_PATH:-\./).*?(/tests})')
    s=re.sub(name_pattern,'\\1{{ project[\'name\'] }}\\2',s)


    return s

# @register
def new_project2():
    # 拷贝一份并重命名project_name
    if os.path.exists(project['name']):
        print(project['name']+' folder already exists')
        return False

    subprocess_run("cp -rf %s/template/project %s"%(SCRIPT_LOCATION,project['name']))
    subprocess_run("mv %s/project %s/%s"%(project['name'],project['name'],project['name']))

    # 对于新的拷贝
    project_path = os.path.join(project['name'])
    alowed_pattern=re.compile(r'.*\.(?:txt|cfg|ini|rst|md)$')

    for root,dirs,files in os.walk(project_path):
        print root,dirs,files, '\n\n'
        files[:] = [f for f in files if alowed_pattern.match(f)]

        for file in files:
            with open(os.path.join(root,file),'r') as f:
                # print(cummutils_to_jinja(f.read()))
                s=Template(cummutils_to_jinja(f.read())).render(project=project)
                # print(s)
            with open(os.path.join(root,file),'w') as f:
                f.write(s)



def update_project():
    # 对于新的拷贝
    config.check_config('config.yml')
    project=config.project
    # try:
    #     subprocess_check_run("mv project %s"%(project['name']))
    # except:
    #     print("please your ide to refactor the package name.")
    print("Please use your IDE to refactor the package name.")


    project_path = '.'
    # alowed_pattern=re.compile(r'.*\.(?:txt|cfg|ini|rst|md|gitignore|coveragerc|testr.conf)$')

    alowed_file=set(['tox.ini', 'setup.cfg',  '.gitignore','.coveragerc','.testr.conf'])


    for file in alowed_file:
        with open(os.path.join(file),'r') as f:
            s=Template(cummutils_to_jinja(f.read())).render(project=project)
        with open(os.path.join(file),'w') as f:
            f.write(s)


    # for root,dirs,files in os.walk(project_path):
    #     files[:] = [f for f in files if alowed_pattern.match(f)]
    #     print files
    #     for file in files:
    #         with open(os.path.join(root,file),'r') as f:
    #             s=Template(cummutils_to_jinja(f.read())).render(project=project)
    #         with open(os.path.join(root,file),'w') as f:
    #             f.write(s)

def new_project(name):
    # 拷贝一份并重命名project_name
    if os.path.exists(name):
        print(name+' folder already exists')
        return False

    subprocess_run("cp -rf %s/template/project %s"%(SCRIPT_LOCATION,name))
    subprocess_run("mv %s/project %s/%s"%(name,name,name))

    current=os.path.abspath('.')
    os.chdir(name)

    # command="cp -ir %s/template/project/*.* ./"%(SCRIPT_LOCATION)
    # subprocess_shell(command)

    with open('config.yml','r') as f:
        s=f.read()
        name_pattern=re.compile(r'(name\s*:\s*).*?(\n)')
        s=re.sub(name_pattern,'\\1%s\\2'%name,s)
    with open('config.yml','w') as f:
        f.write(s)

    update_project()
    print("Finished. If you want to specify more details, please edit the config.yml file and then run \"ly up \"to update the project init.")
    os.chdir(current)
    return


def manage():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    python project manager
    """
    # todo: 改进: 按字典键排序生成值的列表.
    commands=_functions
    run(commands,description=description)


if __name__ == '__main__':
    pass










## ===== start =========

# 初始化配置

# project_json='''
# {
# 'name': 'new'
#
# }
# '''
#
#
# class Project(object):
#     def __init__(self):
#         self.x=0
#
# import json
# project=Project()


# print(json.loads(project_json))
# project.__dict__=json.loads(project_json)


# print (project.__dict__)
#
# exit(0)

# class的__dict__只是字段, 并且可以直接赋值. 和字典一样. json.dumps(c.__dict__), c.__dict__=json.loads(s), 就可以

# class Project(dict):
#     def __init__(self):
#         pass
#
# project=Project()

#  todo: python字典和对象


