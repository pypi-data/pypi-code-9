# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
'''
 * trd.py source file
 *
 * Copyright (c) 2014-2015 USTC-CMET
 * This file is part of the Automatic Essay Scoring Engine.
 * Significant contributions : Cheng Ding, WeiWei Duan
 *
 * History:
 * --------
 * 2015/05/31 - created (Cheng Ding)
'''

import re
import os

from .. import utils, corpus

class __BNCCategories(list):
    """
    所有bnc语料
    所有文件只有访问时才会加载
    categories_bnc = __BNCCategories(corpus._path.trd.bnc, __bnc_names_all)
    可下标访问：A00 = categories_bnc[0]，
    可用名称访问：A00 = categories_bnc['A00']，
    数量： size = len(categories_bnc)
    A00.has_sml / A00.has_orgin / A00.has_plain / A00.has_token ==> bool
    A00.sml / A00.orgin / A00.plain / A00.token = string list or None
    """
    
    def __init__(self, bnc_base_dir, names):
        self.extend(names)
        self.__bnc_base_dir = bnc_base_dir
    def __iter__(self):
        def it():
            for i in xrange(len(self)):
                yield self[i]
        return it()
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__getitem__(list.__getitem__(self, key))
        #
        class __BNCObject(object):
            def __init__(self, bnc_base_dir, item_name):
                self.name = item_name
                self.__bnc_base_dir = bnc_base_dir
                self.__dir_path = bnc_base_dir.__getattr__(item_name[0]).__getattr__(item_name[0:2])
                self.__sml_path = self.__dir_path.__getattr__(item_name)
                self.__orgin_path = self.__dir_path.__getattr__(item_name + '.orgin')
                self.__plain_path = self.__dir_path.__getattr__(item_name + '.plain')
                self.__token_path = self.__dir_path.__getattr__(item_name + '.token')
                self.has_sml = self.__sml_path != None
                self.has_orgin = self.__orgin_path != None
                self.has_plain = self.__plain_path != None
                self.has_token = self.__token_path != None
            def __getattr__(self, name):
                ls_path = None
                if name == 'sml':
                    ls_path = self.__sml_path
                elif name == 'orgin':
                    ls_path = self.__orgin_path
                elif name == 'plain':
                    ls_path = self.__plain_path
                elif name == 'token':
                    ls_path = self.__token_path
                else:
                    raise AttributeError
                ls = ls_path and [x for x in utils.read_once(ls_path, False, True)] or None
                self.__setattr__(name, ls)
                return ls
        #这里不缓存到类中，因为这个bnc语料太大
        return __BNCObject(self.__bnc_base_dir, key)


class __WSJPlainTextCategories(list):
    
    def __init__(self, base_dir, names):
        self.extend(names)
        self.__base_dir = base_dir
    def __iter__(self):
        def it():
            for i in xrange(len(self)):
                yield self[i]
        return it()
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__getitem__(list.__getitem__(self, key))
        #
        class __WSJObject(object):
            def __init__(self, base_dir, item_name):
                self.name = item_name
                self.__base_dir = base_dir
                self.__dir_path = base_dir.__getattr__(item_name[4:6])
                self.__plain_path = self.__dir_path.__getattr__(item_name)
            def __getattr__(self, name):
                ls_path = None
                if name == 'plain':
                    ls_path = self.__plain_path
                else:
                    raise AttributeError
                ls = ls_path and [x for x in utils.read_once(ls_path, False, True, "iso-8859-1")] or None
                self.__setattr__(name, ls)
                return ls
        #这里不缓存到类中，因为这个bnc语料太大
        return __WSJObject(self.__base_dir, key)

#所有bnc语料
__bnc_names_all = [os.path.basename(x) for x in utils.path_walk(corpus._path.trd.bnc) if len(os.path.basename(x)) == 3]
categories_bnc = __BNCCategories(corpus._path.trd.bnc, __bnc_names_all)

#所有WSJPlainText语料
_wsj_names_all = [os.path.basename(x) for x in utils.path_walk(corpus._path.trd.WSJPlainText) if os.path.basename(x).startswith('wsj_')]
categories_wsj_plain = __WSJPlainTextCategories(corpus._path.trd.WSJPlainText, _wsj_names_all)

#所有ChinaDaily语料
categories_chinadaily = [x.strip() for x in re.findall('<!\[CDATA\[(.*?)\]\]>',
                                   ' '.join(x for x in utils.read_once(corpus._path.trd.chinadaily.__getattr__('chinadaily.xml'), False, True, "utf-8")),
                                   re.DOTALL) if x.strip()]

if __name__ == "__main__":
    print('categories_bnc[0].has_token = > ', categories_bnc[0].has_token)
    print('categories_bnc[0].token[0] = > ', categories_bnc[0].token[0])
    print('categories_bnc[\'A00\'].token[0] =>', categories_bnc['A00'].token[0])
