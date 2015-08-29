import ffi
libc=ffi.open("libc.so")

try:
    errno__ = libc.var("i", "errno")
    def errno_(val=None):
        if val is None:
            return errno__.get()
        errno__.set(val)
except OSError:
    __errno = libc.func("p", "__errno", "")
    def errno_(val=None):
        if val is None:
            p = __errno()
            buf = ffi.as_bytearray(p, 4)
            return int.from_bytes(buf)
        raise NotImplementedError
