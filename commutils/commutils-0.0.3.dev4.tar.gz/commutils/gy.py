#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


'''
api: curl -u "$username:$token" https://api.github.com/user/repos -d '{"name":"'$repo_name'"}'

https://viget.com/extend/create-a-github-repo-from-the-command-line

github 工具, hub: https://hub.github.com/, 一些pull-request等操作以后再仔细看之后补全. 虽然可以加上alias git=hub, 但是这里还是要用hub, 因为系统不一定定义了别名, 运行的子shell里面也不一定有定义别名.

git 流程规范 http://www.ruanyifeng.com/blog/2015/08/git-use-process.html

force push的注意事项: http://willi.am/blog/2014/08/12/the-dark-side-of-the-force-push/

本地流程就是分支内commit. 只要init, commit就行了

远程流程就是1.clone, checkout新分支, 2.commit, 3.与主干同步sync, 4.合并commit(rebase), 5.push到远程分支, 最后发出pull-request

对远程:
1. clone, 或者init_remote (init, create or add_remote, push), 注意第一个init最好要是空的, 之后再commit, push
2. 要提交到远端用branchpush做完之后的四步.

对于直接远程直接master开发: http://www.ruanyifeng.com/blog/2012/07/git.html
不要在master上面开发, master只做合并, 测试, 修bug.
开发用dev分支. 合并dev的时候可以不提交远程直接在本地合并, commit, rebase, merge,
或者用github的功能总是推到远程进行合并.

-------------
本地操作流程
分支合并都用--no-ff 参数
dev: 创建, 合并
　　git checkout -b develop master
　　git checkout master
　　git merge --no-ff develop

feature: 创建合并, 删除
　　git checkout -b feature-x develop

    git checkout develop
　　git merge --no-ff feature-x

　　git branch -d feature-x

release: 创建, 合并, 删除
　　git checkout -b release-1.2 develop

    git checkout master
　　git merge --no-ff release-1.2
　　# 对合并生成的新节点，做一个标签
　　git tag -a 1.2

    git checkout develop
　　git merge --no-ff release-1.2

　　git branch -d release-1.2

bug: 创建, 合并, 删除
　　git checkout -b fixbug-0.1 master

    git checkout master
　　git merge --no-ff fixbug-0.1
　　git tag -a 0.1.1

    git checkout develop
　　git merge --no-ff fixbug-0.1

　　git branch -d fixbug-0.1

'''

from __future__ import print_function
## 解决utf8的问题
import  six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')



from commutils.cli import (
    register_maker,run,autokwoargs,kwoargs,wrapper_decorator,
    os,sh,StringIO,subprocess,shlex,subprocess_run,subprocess_check_run,
)
register,_functions=register_maker()

## =====================
## 正式任务

VERSION=0.1
# todo: 全局变量的问题. 固定, 带有名字空间. 可进一步查证.
# import进来的函数不能使用本地的全局常量, 函数内部的所有量都在原来的名字空间. import不改变本名. 只是用本地符号引用import进来的本名. 因此原有的全局常量不会被覆盖.

## ====================
## 基础任务

@register
def version(the_version=VERSION):
    """Show the version"""
    return '{0} version {1}'.format(__file__,the_version)

@register
def create():
    # api: curl -u "$username:$token" https://api.github.com/user/repos -d '{"name":"'$repo_name'"}'
    # https://viget.com/extend/create-a-github-repo-from-the-command-line
    # github 工具, hub: https://hub.github.com/
    '''
    create remote github repo for current directory.
    :return:
    '''
    subprocess.check_call(['hub','create'])
    return 'SUCCESS: remote github repo created or existed'

@register
def clone(repo):
    '''
    clone from github
    :param repo:
    :return:
    '''
    subprocess.check_call(['hub','clone',repo])
    return 'SUCCESS: cloned repo from remote'
@register
def fork():
    '''
    fork from github
    :return:
    '''
    subprocess.check_call(['hub','clone'])
    return 'SUCCESS: cloned repo from remote'
@register
@autokwoargs
def commit(m=None):
    '''
    git add & commit all changes to local repo.
    :return:
    '''
    sh.git.add('.')
    sh.git.status()
    if not m:
        subprocess.call(['git', 'commit'])
    else:
        subprocess.call(['git', 'commit','-m',m])

    return "SUCCESS: committed successful"

@register
@autokwoargs
def fixup(m=None):
    # todo: 完善fixup和autosquash
    '''
    git add & commit all changes to local repo.
    :return:
    '''
    sh.git.add('.')
    sh.git.status()
    if not m:
        subprocess.call(['git', 'commit','--fixup'])
    else:
        subprocess.call(['git', 'commit','--fixup','-m',m])

    return "SUCCESS: committed successful"


@register
# @kwoargs('from_branch')
def newbranch(branch_name,from_branch='master'):
    '''
    from the newest master checkout a new branch named branch_name, 要先pull
    :param branch_name:
    :return:
    '''
    # if not from_branch:
    #     from_branch='master'
    subprocess.check_call(['git','checkout',from_branch])
    flag='y'
    try:
        subprocess.check_call(['git','pull'])
    except:
        print("ERROR: no remote source specified")
        flag=raw_input("do you want to continue?")
    if flag=='y' or flag=='yes':
        subprocess.check_call(['git','checkout','-b',branch_name])
        return "SUCCESS: new branch %s created and checked out"%branch_name
    else:
        return

@register
def init():
    '''
    init a new local repo.
    :return:
    '''
    # subprocess.call['git','init']
    if len(os.listdir('.')) == 0:
        subprocess.check_call(['touch','readme.md'])
    subprocess.check_call(['git','init'])
    commit(m='init commit')
    return "SUCCESS: inited a new project."
@register
def add_remote():
    '''
    add remote repo
    :return: the status whether successful
    '''
    project_name=os.path.basename(os.path.abspath('.'))
    # todo: 异常处理
    subprocess.call(['git','remote','add','origin','git@github.com:lhrkkk/%s.git'%project_name])
    subprocess.check_call(['git', 'remote', '-v'])
    return "SUCCESS: pushed to remote "
@register
def browse():
    '''
    hub browse
    :return:
    '''
    subprocess.check_call(['hub','browse'])
@register
def pull():
    '''
    wrapper for git pull
    :return:
    '''
    subprocess_run('git pull')

@register
def reset():
    # to1do: implement the reset
    '''
    :return:
    '''
    subprocess_run("git reset")
    pass
@register
def reset_tree():
    # todo:
    subprocess_run("git checkout -f HEAD")

@register
def diff():
    # todo: implement the diff
    '''
    :return:
    '''
    subprocess_check_run('git diff')
@register
def find_branch_name():
    return subprocess.check_output(shlex.split("git rev-parse --abbrev-ref HEAD")).strip().decode()

@register
@autokwoargs
def simplepush(force=False):
    '''
    push 当前分支到远端.
    :param force:
    :return:
    '''
    # git push --force origin myfeature
    branch_name=find_branch_name()
    if not force:
        subprocess.call(['git','push','-u','origin',branch_name])
    else:
        subprocess.call(['git','push','--force','origin',branch_name])

    return
@register
def log():
    '''
    彩图显示全局的分支和commit图
    :return:
    '''
    subprocess_run("git log --graph --oneline --all")
@register
def branch_is_exist(branch_name):
    # git rev-parse --verify <branch_name> # 返回值等于0的时候存在. 和下面命令等价
    command="git show-ref --verify --quiet refs/heads/"+branch_name
    try:
        subprocess_check_run(command)
        return True
    except:
        return False
@register
def checkout(branch):
    subprocess_check_run("git checkout "+branch)
@register
def delete_branch(branch):
    subprocess_check_run("git branch -d "+branch)
@register
def git_tag(tag):
    subprocess_check_run("git tag -a "+tag)
    return


@register
def sync():
    '''
    sync remote changes to local branch.
    :return:
    '''
    # git fetch origin
    commit()
    subprocess.check_call(['git','fetch','origin'])
    # git rebase origin master
    subprocess.check_call(['git','rebase','origin/master'])
    return "SUCCESS: synced to remote repo."

@register
def rebase():
    # git rebase -i origin/master
    # todo: cherry-pick 什么意思
    commit()
    subprocess.check_call(['git','rebase','-i','--autosquash','origin/master'])
    return


### ==========
# 组合任务
@register
def init_remote():
    init()
    create()
    add_remote()
    simplepush()

## 和别人合作步骤: 1.下载新建分支,clone, newbranch 2.提交*n, sync, branchpush(sync, rebase, push, ), 3. 发出pull-request
## 自己分支合并步骤: 1. 初始化init/初始化远程init_remote, 新建dev分支 2. 提交*n, 同步, rebase,(push) 3.merge
## 发布步骤:push


# commit, sync, (rebase), push/merge, 后一个必须有前一个作为前提.

# 最终就是, commit, sync, push/merge

@register
@autokwoargs
def push(force=False):
    '''
    平时的时候应该维护dev的分支, 如果要merge到主分支的时候或者到push远程的时候, 则rebase成一个点.
    :return:
    '''
    try:
        commit()
    except:
        pass
    sync()
    rebase()
    simplepush(force=force)


## merge别人的code的时候往往会先在本地把master merge进分支进行合并, 成功后, 再把分支merge进master
@register
def merge2(to_branch='master'):
    '''
    本地开发的小branch 直接merge进master, 不去远程merge了.
    :return:
    '''
    branch_name=find_branch_name()
    commit()
    sync()
    rebase()
    # subprocess_run("git merge "+to_branch)
    subprocess_run("git checkout "+to_branch)
    # print("git merge --no-ff "+branch_name)
    # print( shlex.split("git merge --no-ff "+branch_name))
    subprocess_run("git merge --no-ff "+branch_name)

@register
def merge():

    branch_name=find_branch_name()
    if 'feature' in branch_name:
        feature(merge=True, branch_name=branch_name)
    elif 'bug-fix' in branch_name:
        bug_fix(merge=True,branch_name=branch_name)
    elif 'dev' in branch_name:
        dev(merge=True,branch_name=branch_name)
    elif 'release' in branch_name:
        release(merge=True,branch_name=branch_name)


@register
@autokwoargs
def master():
    checkout('master')
    # if merge:
    #     branch_merge_to('master')
@register
@autokwoargs
def dev(merge=False,branch_name='dev'):
    # dev is from and merge to master by default
    if not branch_is_exist('dev'):
        newbranch('dev')
    checkout('dev')
    if merge:
        merge2('master')
@register
@autokwoargs
def feature(merge=False,delete=False,name=None,branch_name='feature'):
    if name:
        branch_name+='-'+name
    father_name='dev'
    if not branch_is_exist(branch_name):
        newbranch(branch_name,from_branch=father_name)
    checkout(branch_name)
    if merge:
        merge2(father_name)
    if delete:
        checkout(father_name)
        delete_branch(branch_name)
@register
@autokwoargs
def release(merge=False,delete=False,tag=None,branch_name='release'):
    if tag:
        branch_name+='-'+tag
    father_name='dev'
    if not branch_is_exist(branch_name):
        newbranch(branch_name,from_branch=father_name)
    checkout(branch_name)
    if merge:
        merge2('dev')
        merge2('master')
        # if tag:
        git_tag(branch_name)
    if delete:
        checkout(father_name)
        delete_branch(branch_name)
@register
@autokwoargs
def bug_fix(merge=False,delete=False,tag=None,branch_name='bug-fix'):
    if tag:
        branch_name+='-'+tag
    father_name='master'

    if not branch_is_exist(branch_name):
        newbranch(branch_name,from_branch=father_name)
    checkout(branch_name)
    if merge:
        merge2('dev')
        merge2('master')
        # if tag:
        git_tag(branch_name)
    if delete:
        checkout(father_name)
        delete_branch(branch_name)

@register
def new(branch_name):

    if 'feature' in branch_name:
        feature(branch_name=branch_name)
    elif 'bug-fix' in branch_name:
        bug_fix(branch_name=branch_name)
    elif 'dev' in branch_name:
        dev(branch_name=branch_name)
    elif 'release' in branch_name:
        release(branch_name=branch_name)



'''
dev: 创建, 合并
　　git checkout -b develop master
　　git checkout master
　　git merge --no-ff develop

feature: 创建合并, 删除
　　git checkout -b feature-x develop

    git checkout develop
　　git merge --no-ff feature-x

　　git branch -d feature-x

release: 创建, 合并, 删除
　　git checkout -b release-1.2 develop

    git checkout master
　　git merge --no-ff release-1.2
　　# 对合并生成的新节点，做一个标签
　　git tag -a 1.2

    git checkout develop
　　git merge --no-ff release-1.2

　　git branch -d release-1.2

bug: 创建, 合并, 删除
　　git checkout -b fixbug-0.1 master

    git checkout master
　　git merge --no-ff fixbug-0.1
　　git tag -a 0.1.1

    git checkout develop
　　git merge --no-ff fixbug-0.1

　　git branch -d fixbug-0.1

'''


def main():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    a git wrapper

    """
    # commands = [i.__name__ for i in locals().values() if callable(i)]




    # import operator
    # todo: 改进: 按字典键排序生成值的列表.
    commands=_functions
    run(commands,description=description)

if __name__ == '__main__':
    main()
