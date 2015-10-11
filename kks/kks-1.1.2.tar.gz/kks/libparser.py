# coding=utf8

"""
    kks.libparser
    ~~~~~~~~~~~~~

    Parse post source, return title, time, tag, body(markdown).
"""

import os
from ctypes import *
from distutils.sysconfig import get_python_lib


dll_path = os.path.join(get_python_lib(), 'kkslibparser.so')

libparser = CDLL(dll_path)


class Post(Structure):
    _fields_ =  (
        ('title', c_void_p),
        ('time', c_void_p),
        ('tag', c_void_p),
        ('body', c_char_p),
        ('titlesz', c_int),
        ('timesz', c_int),
        ('tagsz', c_int)
    )


post = Post()


def parse(src):
    """Note: src should be ascii string"""
    rt = libparser.parse(byref(post), src)
    return (
        rt,
        string_at(post.title, post.titlesz),
        string_at(post.time, post.timesz),
        string_at(post.tag, post.tagsz),
        post.body
    )
