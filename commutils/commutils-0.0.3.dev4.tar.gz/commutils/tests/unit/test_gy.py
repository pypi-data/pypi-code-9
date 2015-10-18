#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils import gy

class TestGy(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_version(self):
        return
        gy.version(the_version=VERSION)


    def test_create(self):
        return
        gy.create()


    def test_clone(self):
        return
        gy.clone(repo)


    def test_fork(self):
        return
        gy.fork()


    def test_commit(self):
        return
        gy.commit(m=None)


    def test_newbranch(self):
        return
        gy.newbranch(branch_name,from_branch='master')


    def test_init(self):
        return
        gy.init()


    def test_add_remote(self):
        return
        gy.add_remote()


    def test_browse(self):
        return
        gy.browse()


    def test_pull(self):
        return
        gy.pull()


    def test_init_remote(self):
        return
        gy.init_remote()


    def test_reset(self):
        return
        gy.reset()


    def test_reset_tree(self):
        return
        gy.reset_tree()


    def test_diff(self):
        return
        gy.diff()


    def test_sync(self):
        return
        gy.sync()


    def test_rebase(self):
        return
        gy.rebase()


    def test_find_branch_name(self):
        return
        gy.find_branch_name()


    def test_push(self):
        return
        gy.simplepush(force=False)


    def test_branchpush(self):
        return
        gy.push(force=False)


    def test_branch_merge_to(self):
        return
        gy.merge2(to_branch='master')


    def test_merge(self):
        return
        gy.merge2()


    def test_log(self):
        return
        gy.log()


    def test_branch_is_exist(self):
        return
        gy.branch_is_exist(branch_name)


    def test_checkout(self):
        return
        gy.checkout(branch)


    def test_delete_branch(self):
        return
        gy.delete_branch(branch)


    def test_git_tag(self):
        return
        gy.git_tag(tag)


    def test_master(self):
        return
        gy.master()


    def test_dev(self):
        return
        gy.dev(merge=False,branch_name='dev')


    def test_feature(self):
        return
        gy.feature(merge=False,delete=False,name=None,branch_name='feature')


    def test_release(self):
        return
        gy.release(merge=False,delete=False,tag=None,branch_name='release')


    def test_bug_fix(self):
        return
        gy.bug_fix(merge=False,delete=False,tag=None,branch_name='bug-fix')


    def test_new(self):
        return
        gy.new(branch_name)


    def test_gy(self):
        return
        gy.main()



if __name__ == '__main__':
    unittest.main()



