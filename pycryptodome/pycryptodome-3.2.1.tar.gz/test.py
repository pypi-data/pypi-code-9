from Crypto.Hash import CMAC
from binascii import unhexlify, hexlify

key = unhexlify("2b7e151628aed2a6abf7158809cf4f3c")
c = CMAC(key,
