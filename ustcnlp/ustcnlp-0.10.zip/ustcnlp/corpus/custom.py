# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
'''
 * custom.py source file
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

def read_meta_content_file(name, file_path):
    '''
    读取作文样本
    元数据所在行的前一行必须为空白行或者元数据为文件的第一行
    元数据只可以占一行
    内容中不可有空行
    ---------------
    返回一个列表, 元素为所含的每一条含meta的记录，访问时键名全小写
    成员访问：lst.name==>文件名
    成员访问：lst[0] -->纯文本字符串
    成员访问：lst[0].with_tag
    成员访问：lst[0].school
    '''
    
    class __OneList(list):
        pass
    class __StrObj(utils.TYPE_UNICODE):
        pass
    def __read(meta, content, lst):
        if meta.strip() and content.strip():
            meta = meta.strip()
            content = content.strip()
            es = __StrObj(re.sub('\[.*?\]', '', content))
            es.with_tag = content
            es.meta = meta
            for k, v in re.findall('<([A-Za-z0-9_]+) (.*?)>', meta) or dict().items():
                es.__setattr__(k[0] != '_' and k.lower() or k, v)
            lst.append(es)
    lst, meta, content = __OneList(), '', ''
    for line in utils.read_once(file_path, False, False):
        if not line.strip():
            __read(meta, content, lst)
            meta, content = '', ''
        elif not meta:
            meta = line.strip()
            meta = re.sub('<(.*?)->', '', meta)
            meta = meta.strip()
        else:
            content += line.replace("\r\n", "\n")
    __read(meta, content, lst)
    lst.name = name
    return lst

def read_misspell_file(name, file_path):
    '''
    读取拼写样本
    元数据所在行的前一行必须为空白行或者元数据为文件的第一行
    元数据只可以占一行
    句子占一行
    每个错误占一行（可选），错误行：单词序号（0开始） 错误词 建议词1 建议词2（可选）建议词3（可选）
    ---------------------
    整个文件是strict的，当前仅当：每个元素都strict，并且要么同时含error要么同时不含error
    元素是strict的，当前仅当：无错误或者每个错误仅有一个建议词
    ---------------------
    返回一个列表, 元素为所含的每一条拼写语料，访问时键名全小写
    成员访问：lst.strict==>列表是否为strict语料
    成员访问：lst.is_error==>列表是否为错误语料
    成员访问：lst.name==>文件名
    成员访问：lst[0].strict
    成员访问：lst[0].sentence==>单词list
    成员访问：lst[0].error==>为一字典，键为整数单词序号，值为建议词，值在strict时为str,非strict时为list
    '''
    meta = read_meta_content_file(name, file_path)
    for i in xrange(len(meta)):
        sid, content = meta[i].sentence, meta[i].split('\n')
        es = utils.BaseClass()
        es.sid = sid
        es.sentence = content[0].strip().split(' ')
        es.error = dict()
        es.strict = True
        for j in xrange(1, len(content)):
            item = content[j].split(' ')
            assert(es.sentence[int(item[0])] == item[1])
            es.error[int(item[0])] = (len(item) > 3 and item[2:]) or (len(item) == 3 and item[2]) or None
            if len(item) != 3 and es.strict:
                es.strict = False
        meta[i] = es
    #有一个即is_error
    meta.is_error = False
    for es in meta:
        if es.error:
            meta.is_error = True
            break
    #每个元素都strict，并且要么同时含error要么同时不含error
    meta.strict = True
    for es in meta:
        meta.strict = meta.strict and es.strict
        meta.strict = (not es.error) == (not meta.is_error)
        if not meta.strict:
            break
    return meta

class MetaCategories(list):
    """
    含Meta文件的目录
    所有文件只有访问时才会加载，访问一次后会缓存
    categories_essay = __MetaCategories('essay', corpus._path.custom.essay)
    可下标访问：digitalAge = categories_essay[0]，
        得到__MetaCategories('TheDigitalAge', corpus._path.custom.essay.TheDigitalAge)
        若为meta文件则得到read_meta_content_file(corpus._path.custom.essay.TheFilePath)
    可用名称访问：digitalAge = categories_essay['TheDigitalAge']
    数量： size = len(categories_essay)
    """
    
    def __init__(self, name, base_dir, read_fun=read_meta_content_file,
                 test_file=lambda d:d and d[0] not in ['!', '.'], test_dir=lambda d:d and d[0] not in ['!', '.']):
        self.obj = dict()
        self.name = name
        self.__base_dir = base_dir
        self.__read_fun = read_fun
        for d in os.listdir(base_dir):
            if os.path.isfile(base_dir.__getattr__(d)):
                if not test_file or test_file(d):
                    self.append(d)
            else:
                if not test_dir or test_dir(d):
                    self.append(d)
    def __iter__(self):
        def it():
            for i in xrange(len(self)):
                yield self[i]
        return it()
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__getitem__(list.__getitem__(self, key))
        if key.lower() in self.obj:
            return self.obj[key.lower()]
        #
        full = self.__base_dir.__getattr__(key)
        if full:
            if os.path.isdir(full):
                v = self.__class__(key, full)
            else:
                v = self.__read_fun(key, full)
            self.obj[key.lower()] = v
            return v
        else:
            raise AttributeError

categories_essay = MetaCategories('essay', corpus._path.custom.essay)
categories_misspell_wrong = MetaCategories('misspell', corpus._path.custom.misspell, read_misspell_file, lambda d:d.endswith('_wrong'))
categories_misspell_right = MetaCategories('misspell', corpus._path.custom.misspell, read_misspell_file, lambda d:d.endswith('_right'))

if __name__ == "__main__":
    
    print('len(categories_essay) =>', len(categories_essay))
    print('categories_essay[0][0][0].school =>', categories_essay[0][0][0].school)
    print('categories_essay[\'TheDigitalAge\'][\'1_120319_ustc\'][0].school =>',
          categories_essay['TheDigitalAge']['1_120319_ustc'][0].school)
    
    print('categories_misspell_wrong[0][0].sid =>', categories_misspell_wrong[0][0].sid)
    print('categories_misspell_wrong[\'USTC2011Jan_20120330_wrong\'][0].sentence =>',
          categories_misspell_wrong['USTC2011Jan_20120330_wrong'][0].sentence)
    print('categories_misspell_wrong[0][0].error =>', categories_misspell_wrong[0][0].error)
    print('categories_misspell_wrong[0].strict =>', categories_misspell_wrong[0].strict)
    print('categories_misspell_wrong[0][0].strict =>', categories_misspell_wrong[0][0].strict)
