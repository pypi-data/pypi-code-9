# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

def d2cpp(data, cpp_source_name, ziped=True, data_fun_name=('get_extern_data', 'release_extern_data'), autolink=True, mod='wb+'):
    '''
    把二进制流转成cpp文件，以嵌入到c/cpp程序中
    '''
    import cStringIO
    import struct
    orgin_size = len(data)
    if ziped:
        import zlib
        data = zlib.compress(data)
        zipped_size = len(data)
    data_io = cStringIO.StringIO()
    data_io.write(data)
    if data_io.tell() % 8 != 0:
        data_io.write(b'\0' * (8 - data_io.tell() % 8))
    data_io.seek(0)
    #
    source_file = open(cpp_source_name, mod)
    i = 0
    s = data_io.read(8)
    source_file.write(b'/*\n')
    source_file.write(b'  To get data: extern void* %s()\n' % data_fun_name[0])
    source_file.write(b'  To release data: extern void %s(void* data)\n' % data_fun_name[1])
    source_file.write(b'  see ae.utils.py for detail\n')
    source_file.write(b'  */\n')
    source_file.write(b'static unsigned long long EXTERN_DATA_%s_%s[]={\n' % (data_fun_name[0], data_fun_name[1]))
    while s != b'':
        q = struct.unpack('Q', s)
        if i and (i % 10) == 0:
            source_file.write(b', \n    0x%016X' % q)
        elif i:
            source_file.write(b', 0x%016X' % q)
        else:
            source_file.write(b'    0x%016X' % q)
        i += 1
        s = data_io.read(8)
    source_file.write(b'\n};\n\n')
    if ziped:
        source_file.write(b'#include <zlib/zlib.h>\n')
        source_file.write(b'#include <stdlib.h>\n')
        source_file.write(b'void* %s()\n' % data_fun_name[0])
        source_file.write(b'{\n')
        source_file.write(b'    Bytef* dest = (Bytef*)malloc(%d);\n' % orgin_size)
        source_file.write(b'    uLongf destLen = %d;\n' % orgin_size)
        source_file.write(b'    uncompress(dest, &destLen, (Bytef*)EXTERN_DATA_%s_%s, %d);\n' % (data_fun_name[0], data_fun_name[1], zipped_size))
        source_file.write(b'    return dest;\n')
        source_file.write(b'}\n')
        source_file.write(b'void %s(void* data)\n' % data_fun_name[1])
        source_file.write(b'{\n')
        source_file.write(b'    free(data);\n')
        source_file.write(b'    return;\n')
        source_file.write(b'}\n')
    else:
        source_file.write(b'void* %s()\n' % data_fun_name[0])
        source_file.write(b'{\n')
        source_file.write(b'    return EXTERN_DATA_%s_%s;\n' % (data_fun_name[0], data_fun_name[1]))
        source_file.write(b'}\n')
        source_file.write(b'void %s(void* data)\n' % data_fun_name[1])
        source_file.write(b'{\n')
        source_file.write(b'    return;\n')
        source_file.write(b'}\n')
    source_file.write(b'unsigned long %s_len()\n' % data_fun_name[0])
    source_file.write(b'{\n')
    source_file.write(b'    return %d;\n' % orgin_size)
    source_file.write(b'}\n')
    if ziped and autolink:
        source_file.write(b'\n')
        source_file.write(b'#ifdef _DEBUG\n')
        source_file.write(b'#pragma comment(lib,"zlibd.lib")\n')
        source_file.write(b'#else\n')
        source_file.write(b'#pragma comment(lib,"zlib.lib")\n')
        source_file.write(b'#endif\n')
    source_file.close()

if __name__ == '__main__':
    pass
