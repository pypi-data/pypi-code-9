from glob import glob
from os import path

try:
    from ._keccak import ffi
except ImportError:
    raise RuntimeError("Required CFFI extension not found. You need to install this package before use. See README.")


try:
    obj_name = glob(path.abspath(path.join(path.dirname(__file__), "sha3*")))[0]
except IndexError:
    raise RuntimeError("Required sha3 extension not found. You need to install this package before use. See README.")

lib = ffi.dlopen(obj_name)

# Length of the output of sha256
output_length = 32
# ffi definition of the output uint array
output = ffi.new("uint8_t[]", output_length)


# SHA3-256 hashing using the Keccak standard
def sha3_256(seed):
    input_ = ffi.new("uint8_t[]", str(seed))
    lib.sha3_256(output, output_length, input_, len(seed))
    buf = ffi.buffer(output, output_length)
    return buf[:]

