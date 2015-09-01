# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import base64
import struct
import re
import json
import io
import os
import ctypes
import threading

from . import utils

class Tag(object):
    #若position是个数组，length需=len(position)。否则position是个整数，length>0。length不会为0。
    #data_str为空或null均不记录，否则记录
    def __init__(self, position, length, sdata=None, idata=0, reserve=0):
        self.position = position
        self.length = length
        assert(isinstance(position, (int, long)) or (length == len(position)))
        self.sdata = sdata
        if self.sdata and isinstance(self.sdata, utils.TYPE_UNICODE):
            self.sdata = self.sdata.encode("utf8")
        self.idata = idata
        self.reserve = reserve
    def __repr__(self):
        rs = "<%s, %s, %s, %s, %s>" % (repr(self.position), repr(self.length), repr(self.sdata), repr(self.idata), repr(self.reserve))
        return rs

class Tags(list):
    __STRING_OF_I = b'<I'
    __STRING_OF_TAG = b'<IIIII'
    __SIZE_OF_I = struct.calcsize(__STRING_OF_I)
    __SIZE_OF_TAG = struct.calcsize(__STRING_OF_TAG)
    __TAG_END = 0x80000000
    def add(self, tag):
        if isinstance(tag, Tag):
            self.append(tag)
    def addp(self, position, length, sdata=None, idata=0, reserve=0):
        tag = Tag(position, length, sdata, idata)
        self.add(tag)
    
    def __init__(self, sbase64=None):
        list.__init__(self)
        if sbase64 and isinstance(sbase64, (utils.TYPE_BASESTRING, utils.TYPE_UNICODE)):
            self.__read_base64(sbase64)
    
    def __str__(self):
        '''
        编码tags为base64字符串
        '''
        bytes_shift = (len(self) + 1) * Tags.__SIZE_OF_TAG
        src = io.BytesIO()
        #第一遍，构建数组
        for tag in self:
            if not isinstance(tag.position, (int, long)):
                position = bytes_shift | Tags.__TAG_END
                bytes_shift += len(tag.position) * Tags.__SIZE_OF_I
                length = len(tag.position)
            else:
                position = tag.position
                length = tag.length
            if tag.sdata:
                sdata = bytes_shift
                bytes_shift += len(tag.sdata) + 1
            else:
                sdata = 0
            idata = tag.idata
            reserve = tag.reserve
            src.write(struct.pack(Tags.__STRING_OF_TAG, position, length, sdata, idata, reserve))
            bytes_shift -= Tags.__SIZE_OF_TAG
        #结束tag
        src.write(struct.pack(Tags.__STRING_OF_TAG, Tags.__TAG_END, 0, 0, bytes_shift - Tags.__SIZE_OF_TAG, 0))
        #第二遍，附加数据
        for tag in self:
            if not isinstance(tag.position, (int, long)):
                for p in tag.position:
                    src.write(struct.pack(Tags.__STRING_OF_I, p))
            if tag.sdata:
                src.write(tag.sdata)
                src.write(b'\0')
        src.seek(0)
        z = src.read()
        return base64.b64encode(z)
    
    def __read_base64(self, sbase64):
        '''
        解码base64字符串为tags
        '''
        #解码base64
        if isinstance(sbase64, utils.TYPE_UNICODE):
            sbase64 = sbase64.encode("utf8")
        bindata = base64.b64decode(sbase64)
        bs = 0
        while True:
            position, length, sdata, idata, reserve = struct.unpack(Tags.__STRING_OF_TAG, bindata[bs:bs + Tags.__SIZE_OF_TAG])
            if position == Tags.__TAG_END:
                break
            elif position > Tags.__TAG_END:
                position_shift = position & (Tags.__TAG_END - 1)
                position = list()
                for i in xrange(length):
                    shift = position_shift + Tags.__SIZE_OF_I * i
                    position.append(struct.unpack(Tags.__STRING_OF_I, bindata[bs + shift:bs + shift + Tags.__SIZE_OF_I])[0])
            if sdata:
                bytes_shift = bs + sdata
                while bindata[bytes_shift] != b'\0':
                    bytes_shift += 1
                sdata = bindata[bs + sdata:bytes_shift]
            else:
                sdata = None
            self.append(Tag(position, length, sdata, idata, reserve))
            bs += Tags.__SIZE_OF_TAG

class Manager(object):
    managerlib = None
    serialize_types = {101:Tags}
    check_condition = threading.Condition()
    @classmethod
    def test(cls):
        cls.__check_lib()
    
    @classmethod
    def __check_lib(cls):
        cls.check_condition.acquire()
        if not Manager.managerlib:
            Manager.managerlib = utils.load_cdll(os.path.dirname(__file__) + os.path.sep + 'manager.ae',
                ('load', [ctypes.c_char_p], None),
                ('unload', None, None),
                ('process_task', [ctypes.c_char_p, ctypes.c_char_p], ctypes.c_void_p),
                ('free_result', [ctypes.c_void_p], None),
                ('get_output', [ctypes.c_int32], ctypes.c_void_p)
            )
            Manager.managerlib.load('')
        cls.check_condition.release()
    
    @classmethod
    def get_outputs(cls):
        cls.__check_lib()
        rs, idx, outp = list(), 1, cls.managerlib.get_output(0)
        while outp:
            rs.append(ctypes.string_at(outp))
            outp = cls.managerlib.get_output(idx)
            idx += 1
        return rs
    
    @classmethod
    def process_task(cls, method, context=None, **params):
        cls.__check_lib()
        if context:
            params['sContext'] = context
        #编译params为json格式字符串
        for k in params.keys():
            v = params[k]
            if isinstance(v, (int, long)):
                itype = 2
                v = int(v)
            elif isinstance(v, float):
                itype = 3
                v = float(v)
            else:
                itype = 0
                for ik, iv in cls.serialize_types.items():
                    if isinstance(v, iv):
                        itype = ik
                        v = str(v)
                        break
                if itype == 0:
                    itype = 1
                    v = str(v)
                    if isinstance(v, utils.TYPE_UNICODE):
                        v = v.encode('utf8')
            params[k] = {'type':itype, 'data':v}
        params = json.dumps({'params':params}, ensure_ascii=False)
        #调用链接库进行处理
        rsp = cls.managerlib.process_task(method, utils.TYPE_BASESTRING(params))
        rs = ctypes.string_at(rsp)
        cls.managerlib.free_result(rsp)
        rs = json.loads(rs, object_pairs_hook=lambda d:d)
        for index, value in enumerate(rs):
            v = dict(value[1])
            data = v['data']
            itype = v['type']
            iv = cls.serialize_types.get(itype, None)
            if iv:
                data = iv(data)
            rs[index] = value[0], data
        return rs

def test():
    #
    tags = Tags()
    tags.addp(0, 5, 'Hello', 0)
    tags.addp(5, 1, ',', 0)
    tags.addp(7, 5, 'World', 0)
    tags.addp(12, 1, '!', 0)
    enc = str(tags)
    assert(enc == 'AAAAAAUAAABkAAAAAAAAAAAAAAAFAAAAAQAAAFYAAAAAAAAAAAAAAAcAAAAFAAAARAAAAAAAAAAAAAAA'
                   + 'DAAAAAEAAAA2AAAAAAAAAAAAAAAAAACAAAAAAAAAAAAQAAAAAAAAAEhlbGxvACwAV29ybGQAIQA=')
    print(repr(Tags(enc)), end='\n\n')
    
    #
    tags = Tags()
    tags.addp([1, 2, 3], 3, 'z好zz', 0)
    tags.addp(0, 5, 'bz', 0)
    tags.addp([4, 5, 6], 3, 'zzz', 56)
    enc = str(tags)
    assert(enc == 'UAAAgAMAAABcAAAAAAAAAAAAAAAAAAAABQAAAE8AAAAAAAAAAAAAAD4AAIADAAAASgAAADgAAAAAAAAAA'
                   + 'AAAgAAAAAAAAAAAJgAAAAAAAAABAAAAAgAAAAMAAAB65aW9enoAYnoABAAAAAUAAAAGAAAAenp6AA==')
    print(repr(Tags(enc)), end='\n\n')
    
    rs = Manager.process_task('tToken tSpelling', 'Hello, Woxrld!', tags=tags, fp=1.0, ip=121)
    print(rs)
    #
    print(Manager.get_outputs())

if __name__ == '__main__':
    for i in xrange(1):
        test()
