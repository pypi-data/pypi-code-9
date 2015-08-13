#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About
~~~~~

**Copyright (c) 2015 by Sanhe Hu**

- Author: Sanhe Hu
- Email: husanhe@gmail.com
- Lisence: MIT


**Compatibility**

- Python2: Yes
- Python3: Yes
    

**Prerequisites**

- None

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function, unicode_literals
from cryptography.fernet import Fernet
from windtalker.messenger import messenger
import hashlib
import base64
import sys
import os
import io

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    input = raw_input
else:
    pass

class SecretKeyNotGivenError(Exception):
    pass

class OverWriteFileError(Exception):
    pass

class PasswordError(Exception):
    pass

class WindTalker():
    """Cipher utility class.
    """
    _secret_key = None
    _encrypt_chunk_size = 1024*1024
    _decrypt_chunk_size = 1398200
    
    def __init__(self):
        pass
    
    def _set_secret_key(self, key):
        """Set your secret key.
        """
        self._secret_key = key
    
    @property
    def secret_key(self):
        return self._secret_key
    
    def set_secret_key(self):
        """User command line to enter your secret key.
        """
        self._set_secret_key(input(
            "Please enter your secret key (case sensitive): "))
    
    def set_encrypt_chunk_size(self, chunk_size):
        """Set the size of how much bytes content stored in your memory. Choose 
        it wisely to fit your memory. I recommend use 100MB for large file.
        """
        self._encrypt_chunk_size = chunk_size
        self._decrypt_chunk_size = self.chunk_size_analysis(self._encrypt_chunk_size)
        
    @property
    def encrypt_chunk_size(self):
        return self._encrypt_chunk_size
    
    @property
    def decrypt_chunk_size(self):
        return self._decrypt_chunk_size
    
    def any_text_to_fernet_key(self, text):
        """Generate url_safe base64 encoded key for fernet symmetric encryption.
        """
        m = hashlib.md5()
        m.update(text.encode("utf-8"))
        fernet_key = base64.b64encode(m.hexdigest().encode("utf-8"))
        return fernet_key
    
    def chunk_size_analysis(self, reading_size):
        """Because windtalker working in streaming mode (read/write content by 
        byte block), so we have to match the reading size with its corresponding
        writing size.
        """
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(b"x" * reading_size)
        return len(token)
                    
    def io_path(self, input_path):
        """Calculate the output windtalker file path. usually just replace the 
        extension with ``.windtalker``.
        """
        abspath = os.path.abspath(input_path)
        fname, _ = os.path.splitext(abspath)
        output_path = fname + ".windtalker"
        return output_path

    def encrypt_file(self, path):
        """Encrypt a file, create an encrypted file with .windtalker file 
        extension.
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")
        
        output_path = self.io_path(path)
        
        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)
        
        cipher = Fernet(self.any_text_to_fernet_key(self.secret_key))
        
        messenger.show("encrypt %s ..." % path)
        
        with open(path, "rb") as f_input:
            with io.FileIO(output_path, "a") as f_output:
                while 1:
                    content = f_input.read(self._encrypt_chunk_size)
                    if content:
                        f_output.write(cipher.encrypt(content))
                    else:
                        break

        messenger.show("\tfinished!")
                    
    def decrypt_file(self, path, output_path):
        """Decrypt a file at ``path``, output to ``output_path``
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")
        
        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)
        
        cipher = Fernet(self.any_text_to_fernet_key(self.secret_key))
        
        messenger.show("decrypt %s ..." % path)
        
        with open(path, "rb") as f_input:
            with io.FileIO(output_path, "a") as f_output:
                while 1:
                    try:
                        content = f_input.read(self._decrypt_chunk_size)
                    except:
                        raise PasswordError("Opps! Wrong magic word.")
                    if content:
                        f_output.write(cipher.decrypt(content))
                    else:
                        break
        
        messenger.show("\tfinished!")
        
if __name__ == "__main__":
    import unittest
    
    class WindTalkerUnittest(unittest.TestCase):
        def test_initialize(self):
            windtalker = WindTalker()
            windtalker._set_secret_key("123456")
            self.assertEqual(windtalker.secret_key, "123456")
            windtalker.set_encrypt_chunk_size(128)
            self.assertEqual(windtalker.encrypt_chunk_size, 128)
            self.assertEqual(windtalker.decrypt_chunk_size, 268)     
             
        def test_chunk_size_analysis(self):
            windtalker = WindTalker()
            self.assertEqual(windtalker.chunk_size_analysis(128), 268)
            self.assertEqual(windtalker.chunk_size_analysis(256), 440)
            self.assertEqual(windtalker.chunk_size_analysis(512), 780)
            self.assertEqual(windtalker.chunk_size_analysis(1024), 1464)
        
        def test_filename(self):
            windtalker = WindTalker()
            input_path = "core.py"
            output_path = windtalker.io_path(input_path)
            dirname, basename = os.path.split(output_path)
            self.assertEqual(basename, "core.windtalker")
                
        def test_encrypt_decrypt_file(self):
            windtalker = WindTalker()
            windtalker._set_secret_key("123456")
            windtalker.encrypt_file("core.py")
            windtalker.decrypt_file("core.windtalker", "core1.py")
            with open("core.py", "r") as f:
                content1 = f.read()
            with open("core1.py", "r") as f:
                content2 = f.read()
            self.assertEqual(content1, content2)
            
        def tearDown(self):
            for path in ["core.windtalker", "core1.py"]:
                try:
                    os.remove(path)
                except:
                    pass
            
    unittest.main()