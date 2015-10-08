#!/usr/bin/env python
from ctypes.util import find_library

from ._gcrypt import ffi
from . import errors

lib = ffi.dlopen(find_library("gcrypt"))

class Cipher(object):
    """
    This class is mostly an implementation of the cipher handler
    as described in the documentation of libgcrypt:
      <https://www.gnupg.org/documentation/manuals/gcrypt/Working-with-cipher-handles.html>

    It is used as a member of the class Context which makes sure everything is correctly
    setup.
    """
    def __init__(self, algo, mode, flags=0):
        """
        algo is a string to be used as the algorithm name, among: https://www.gnupg.org/documentation/manuals/gcrypt/Available-ciphers.html
        mode is a string to be used as the algorithm mode, among https://www.gnupg.org/documentation/manuals/gcrypt/Available-cipher-modes.html
        flags is a bitwise int to be initialized as a OR combination of several flags:
          GCRY_CIPHER_SECURE
          GCRY_CIPHER_ENABLE_SYNC
          GCRY_CIPHER_CBC_CTS
          GCRY_CIPHER_CBC_MAC
        """
        error = ffi.cast("gcry_error_t", 0)
        self.mode = mode
        self.algo = lib.gcry_cipher_map_name(algo)
        self._mode = getattr(lib, u'GCRY_CIPHER_MODE_' + mode)

        self.flags = ffi.cast("unsigned int", flags)
        self.context = ffi.new("gcry_cipher_hd_t *")

        error = lib.gcry_cipher_open(self.context, self.algo, self._mode, self.flags)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)

    def __getitem__(self, item):
        error = ffi.cast("gcry_error_t", 0)
        if item in ['key', 'iv', 'ctr', 'mode']:
            return getattr(self, item, None)

        if item == 'algo':
            return ffi.string(lib.gcry_cipher_algo_name(self.algo))

        if item == 'keylen':
            # the keylen is in bytes nit in bits
            size = ffi.new('size_t *')
            size = lib.gcry_cipher_get_algo_keylen(self.algo)
            return int(size)

        if item == 'blocksize':
            size = ffi.new('size_t *')
            size = lib.gcry_cipher_get_algo_blklen(self.algo)
            return int(size)
            
        raise KeyError("No key named {} found.".format(item))

    def __setitem__(self, item, value):
        error = ffi.cast("gcry_error_t", 0)
        if item == 'key':
            error = lib.gcry_cipher_setkey(self.context[0]
                    , value.encode()
                    , len(value.encode()))
            if error != 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
            self.key = value
            return

        if item == 'iv':
            if value != None:
                error = lib.gcry_cipher_setiv(self.context[0]
                        , value.encode()
                        , len(value.encode()))
                if error != 0:
                    raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
            self.iv = value
            return

        if item == 'ctr':
            error = lib.gcry_cipher_setctr(self.context[0]
                    , value.encode()
                    , len(value.encode()))
            if error != 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
            self.ctr = value
            return
        raise KeyError("Cannot set {}.".format(item))

    def reset(self):
        """
        Set the given handle’s context back to the state it had after the last call to gcry_cipher_setkey and clear the initialization vector.
        Since this is a macro, we will issue the call to the functins, avoiding the macro
          #define gcry_cipher_reset(h) gcry_cipher_ctl ((h), GCRYCTL_RESET, NULL, 0)
        """
        error = ffi.cast("gcry_error_t", 0)
        error = lib.gcry_cipher_ctl(self.context[0], lib.GCRYCTL_RESET, ffi.NULL, 0)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        self['iv'] = None

    def __pad(self, data):
        padlen = self['blocksize'] - (len(data) % self['blocksize']) if len(data) % self['blocksize'] != 0 else self['blocksize']
        data += bytes([padlen] * padlen)
        return data

    def __depad(self, data):
        padlen = ord(data[-1:])
        return data[:len(data) - padlen]

    def encrypt(self, data):
        """
        We want to encrypt data. Since libgcrypt doesn't do padding, we will
        have to do it ourselves. We will use the PKCS#7 padding scheme
        """
        data = self.__pad(data)
        error = ffi.cast("gcry_error_t", 0)
        error = lib.gcry_cipher_encrypt(self.context[0], data, ffi.cast('size_t', len(data)), ffi.NULL, 0)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        return data

    def decrypt(self, data):
        """
        We will decrypt the data received, and remove the padding. 
        """
        error = ffi.cast("gcry_error_t", 0)
        error = lib.gcry_cipher_decrypt(self.context[0], data, ffi.cast('size_t', len(data)), ffi.NULL, 0)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        return self.__depad(data)

    # The following method are used for Authenticated Encryption with Associated Data (AEAD) block cipher modes 
    # which require the handling of the authentication tag and the additional authenticated data
    def aead_authenticate(self, auth_data):
        """
        Process the buffer abuf of length abuflen as the additional authenticated data (AAD) for AEAD cipher modes.

        auth_data is a bytes like object
        """
        error = ffi.cast("gcry_error_t", 0)
        error = lib.gcry_cipher_authenticate(self.context[0]
                , auth_data
                , len(auth_data))
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
