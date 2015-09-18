from cffi import FFI


ffi = FFI()

ffi.set_source("keccak._keccak", None)
ffi.cdef(
    '''
    int sha3_256(uint8_t*, size_t, uint8_t const*, size_t);
    ''')


if __name__ == '__main__':
    ffi.compile()
