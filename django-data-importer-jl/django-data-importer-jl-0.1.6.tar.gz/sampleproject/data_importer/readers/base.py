from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import zip
from builtins import next
from builtins import map
from builtins import *
from builtins import object
# coding: utf-8
import io as _io
from collections import OrderedDict
from data_importer.exceptions import UnknowSource
import unicodedata
from data_importer.utils import to_unicode


class BaseReader(object):

    def __init__(self, f):
        """
        init receive f as a file object
        """
        self.loaded = False
        self._source = None
        self._reader = None
        self._headers = None
        self.__load(f)

    def __iter__(self):
        return self.get_items()

    def __load(self, source):
        """
        Load a file or a file path to self._source.
        Don't touch in this method, some assertions here is really important
        """
        try:
            if isinstance(source, _io.IOBase):
                self._source = source
            if isinstance(source, str):
                self._source = open(source, 'rb')
        except Exception as err:
            raise UnknowSource(err)

        self.loaded = True
        self.set_reader()
        assert self._reader is not None
        assert self.headers is not None  # call self.headers

    def unload(self):
        """
        Close the input file and free resources, it matters for big files :)
        """
        if isinstance(self._source, _io.IOBase):
            self._source.close()
        else:
            self._source = None

        self.loaded = False

    def set_reader(self):
        """
        This method will start file reader if necessary because normally each
        file type can have a existent reader in python and BaseReader can't
        know it.
        This method is called in self.__load after source is read and should set
        self._reader. self.get_items and self.get_header should read self._reader.
        """
        self._reader = open(self._source.name, 'rb')

    def get_value(self, item, **kwargs):
        """
        Receive item from source and should return formated value.
        Can be customized to handle various types. The default just return
        value.

        This method isn't used in base implementation, but readers that have
        different values for data types like xml can use that.
        """
        return item

    def get_item(self, row):
        """
        Given a header and a row return a sorted dict
        """
        def normalize(s):
            if isinstance(s, basestring):
                try:
                    return to_unicode(s.strip())
                except (UnicodeDecodeError, UnicodeEncodeError):
                    return s.strip()
            else:
                return s

        # if we have headers = ['a','b'] and values [1,2,3,4], dict will be
        # {'a':1,'b':2}
        # if we have headers = ['a','b','c','d'] and values [1,2], dict will be
        # {'a':1,'b':2}
        d = OrderedDict(
            [i for i in zip(self.headers, list(map(normalize, row))) if i[0]])
        # since zip can cut tuple to smaller sequence, if we get incomplete
        # lines in file this for over headers put it on row dict
        for k in self.headers:
            if k not in d:
                d[k] = u''
        d.keyOrder = self.headers
        return d

    @property
    def headers(self):
        """
        Should set self._headers and should run only one time.

        Since header normally is first line of the file, we get the first one
        here, but we can't know format that reader should be read, so we just
        do a next on reader.

        This method runs as headers property
        """

        if not self._headers:
            self._headers = list(
                map(self.normalize_string, next(self._reader)))
        return self._headers

    def normalize_string(self, value):
        if not value:
            return ''
        value = value.strip()
        value = value.lower()
        try:
            value = unicodedata.normalize('NFKD', str(value))
        except (UnicodeDecodeError, UnicodeEncodeError):
            value = unicodedata.normalize('NFKD', to_unicode(value))
        value = value.encode('ascii', 'ignore')
        value = value.replace(b' ', b'_')
        return value

    def get_items(self):
        """
        Iterator do read the rows of file. Should return a dict with fields
        name and values. get_items should set headers too.
        """
        raise NotImplementedError
