from cffi import FFI
ffi = FFI()

ffi.set_source("pysplice._splice", '''
    #define _GNU_SOURCE
    #include <fcntl.h>
''')
ffi.cdef("""
    #define SPLICE_F_MOVE ...
    #define SPLICE_F_NONBLOCK ...
    #define SPLICE_F_MORE ...
    #define SPLICE_F_GIFT ...

    typedef int... loff_t;
    ssize_t splice(int fd_in, loff_t *off_in, int fd_out,
                   loff_t *off_out, size_t len, unsigned int flags);
""")

if __name__ == "__main__":
    ffi.compile()
