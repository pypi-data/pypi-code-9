# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
'''
 * dictionary.py source file
 *
 * Copyright (c) 2014-2015 USTC-CMET
 * This file is part of the Automatic Essay Scoring Engine.
 * Significant contributions : Cheng Ding, WeiWei Duan
 *
 * History:
 * --------
 * 2015/05/31 - created (Cheng Ding)
'''

from . import utils

_path = utils.PathObj(utils.path_join(utils.extract_dir(__file__), '../../../../data/dictionary'))

def __get_range_bnc():
    word_to_family = dict()
    family_to_words = dict()
    for line in utils.read_once(_path.RangeBNC.__getattr__('Range_BNC.txt')):
        u = line.lower().split(' ')
        word, family = u[0], u[-1]
        word_to_family[word] = family
        if not family_to_words.has_key(family):
            family_to_words[family] = set()
        family_to_words[family].add(word)
    return word_to_family, family_to_words

__word_to_family, __family_to_words = __get_range_bnc()

#Range_BNC词典
rb_words = set(__word_to_family.keys())
#Range_BNC词族
rb_families = set(__family_to_words.keys())

#获取单词所属的词族
def family(word, empok=False):
    return __word_to_family.get(word.lower(), not empok and word or '')

#获取词族所含的单词
def unfamily(family, rset=True, empok=False):
    s = __family_to_words.get(family.lower(), None)
    if not s:
        s = not empok and set([family.lower()]) or set()
    if rset:
        return s
    else:
        return ' '.join(s)

class mset(set):
    def inc(self, items, reverse=False, lowerin=True):
        '''
        返回items在此词典中（reverse=False）或者不在词典中（reverse=True）的元素列表
        默认判断为items元素转小写后再判断其是否在词典中
        '''
        return filter(lambda d:((d.lower() if lowerin else d) in self) != reverse, items)

def load(dpath, rs_mset=True):
    '''
    加载词典, dpath为词典目录，rs_set为True时返回set否则返回list
    '''
    class mlist(list):
        pass
    v = list()
    started = False
    for line in utils.read_once(dpath):
        if not started:
            started = not line.startswith('#')
        if started:
            v.append(line)
    if v and v[0].startswith('{'):
        import json
        return json.loads(''.join(v))
    else:
        if rs_mset:
            return mset(v)
        else:
            return v
