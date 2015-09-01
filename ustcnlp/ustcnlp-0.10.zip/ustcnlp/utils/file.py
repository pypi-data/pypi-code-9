# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import codecs
import os

####目录操作######

def extract_dir(full_path):
    """
    提取目录
    """
    return os.path.dirname(full_path) + os.path.sep

path_sep = os.path.sep

def path_exists(path):
    return os.path.exists(path)

def path_join(a, *p):
    """
    合并目录
    """
    return os.path.normpath(os.path.join(a, *p))

def path_walk(root_path, end_with=""):
    """
    变量目录下的所有文件（含子目录）
    """
    for root_dirs_files in os.walk(root_path):
        for name in root_dirs_files[2]:
            if not end_with or name.upper().endswith(end_with.upper()):
                yield path_join(root_dirs_files[0], name)

####读写文件######

def read_once(file_path, no_empty=True, strip=True, charset="utf-8", position=0, strict=True):
    """
    读取文本文件中的行到迭代器
    """
    f = codecs.open(file_path, "r+", charset, strict and 'strict' or 'replace')
    if position:
        f.seek(position)
    for line in f:
        if strip:
            line = line.strip()
        if not no_empty or line:
            yield line
    f.close()

def open_write(file_path, charset="utf-8", mod='w+'):
    """
    使用codecs.open以写方式打开文件
    """
    return codecs.open(file_path, mod, charset)

def save_list(lst, save_to, key=lambda d:d + '\n', charset="utf-8", mod='w+'):
    """
    保存一个list中的字符串到一个文件中
    """
    f = open_write(save_to, charset, mod)
    for ln in lst:
        f.write('%s' % key(ln))
    f.close()


#路径工具类
class PathObj(unicode):
    def __init__(self, path):
        unicode.__init__(unicode(path))
    def __getattr__(self, name):
        new_path = path_join(self, name)
        if os.path.exists(new_path):
            new_path = PathObj(new_path)
            self.__setattr__(name, new_path)
            return new_path
        else:
            return None


if __name__ == '__main__':
    pass
