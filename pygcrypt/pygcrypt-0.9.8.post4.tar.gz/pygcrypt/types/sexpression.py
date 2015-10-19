#!/usr/bien/env python
import re
from ctypes.util import find_library

from .._gcrypt import ffi
from .. import errors
from .mpi import MPIint, MPIopaque

lib = ffi.dlopen(find_library("gcrypt"))

class SExpression(object):
    """
    This class is used to manage S-Expression. They are list in lisp but
    generally the car (first element) is the type of the next item.

    It's extremely similar to a hashtable, so we're going to use the dict
    operators __getitem__, __setitem__ and __iter__ to reflect that.

    Howevern we will need some specific works to be done on the __repr__
    part since some specific formating is needed to use a S-expression in
    another one.
    """
    def __init__(self, *args, **kwargs):
        """
        Let's build a new S-Expression. We're going to use sscan to allow
        for detection of parsing errors.

        kwargs might contains various st of args, used to determine which
        function will be called to build the s-expr
        """
        error = ffi.cast("gcry_error_t", 0)
        erroffset = 0
        sexp = ffi.new("gcry_sexp_t *")
        self.fmt = 'DEFAULT'

        if len(args) == 0:
            raise TypeError("SExpression must be created with at least 1 parameters, none given")

        if len(args) == 1 and isinstance(args[0], bytes):
            # We have only one arg, and it's a byte
            error = lib.gcry_sexp_sscan(sexp, ffi.cast("size_t *", erroffset),  args[0], ffi.cast("size_t", len(args[0])))
        elif len(args) == 1 and (ffi.typeof(args[0]) is ffi.typeof("gcry_sexp_t *") or ffi.typeof(args[0]) is ffi.typeof("gcry_sexp_t")):
            self.__sexp = args[0]
            self.fmt = 'ADVANCED'
            return
        else:
            # We need to work a little bit on the args passed to the varidadic part of the call. For that we first need to get all the
            # % items from the first arg.
            items = re.findall(r'%([mMsdubS])', args[0].decode())
            i = 1
            vargs = []
            for item in items:
                if item in ('m', 'M'):
                    # Then, we want a MPI. Will be stored as a signed integer
                    if not isinstance(args[i], MPIint):
                        raise TypeError("Item {} (%{}) should be of type MPIint, got {} instead".format(i, item, type(args[i])))
                    vargs.append(args[i].mpi)
                    i += 1
                    continue
                if item == 's':
                    # We want a string. If it's a str, just encode it
                    data = args[i]
                    if isinstance(data, str):
                        data = data.encode()
                    if not isinstance(data, bytes):
                        raise TypeError("Item {} (%{}) should be of type bytes or str, got {} instead".format(i, item, type(data)))
                    vargs.append(ffi.new("char []", data))
                    i += 1
                    continue
                if item in ('d', 'u'):
                    # We want an int.
                    if not isinstance(args[i], int):
                        raise TypeError("Item {} (%{}) should be of type int, got {} instead".format(i, item, type(args[i])))
                    if item == 'u' and args[i] < 0:
                        raise TypeError("Item {} (%{}) should be of type unsigned int, got a negative number".format(i, item))
                    if item == 'u':
                        vargs.append(ffi.cast("unsigned int", args[i]))
                    else:
                        vargs.append(ffi.cast("int", args[i]))
                    i += 1
                    continue
                if item == 'b':
                    # We need TWO args now.
                    try:
                        if not isinstance(args[i], int):
                            raise TypeError("Item {} (%{}) should be preceded by an int which value is the length of the string".format(i, item))
                        data = args[i+1]
                        if isinstance(data, str):
                            data = data.encode()
                        if not isinstance(data, bytes):
                            raise TypeError("Item {} (%{}) should be of type bytes or str, got {} instead".format(i, item, type(data)))
                        vargs.append(ffi.cast("int", args[i]))
                        vargs.append(ffi.new("char []", data))
                        i += 2
                        continue
                    except IndexError:
                        raise TypeError("Item {} (%{}) should be made of two parts.".format(i, item))
                if item == 'S':
                    # We want a SExpression
                    if not isinstance(args[i], SExpression):
                        raise TypeError("Item {} (%{}) should be a S-Expression, got a {} instead".format(i, item, type(args[i])))
                    if not repr(args[i]).startswith('('):
                        # This is an invalid SExpression
                        raise ValueError("Item {} (%{}) must be an SExpression starting by a '('".format(i, item))
                    vargs.append(args[i].sexp)
                    i += 1
                    continue
            error = lib.gcry_sexp_build(sexp, ffi.cast("size_t *", erroffset), args[0], *vargs)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
        self.__sexp = sexp[0]
        self.fmt = 'ADVANCED'

    def __getattr__(self, attr):
        if attr == 'sexp':
            if ffi.typeof(self.__sexp) == ffi.typeof("gcry_sexp_t *"):
                return self.__sexp[0]
            elif ffi.typeof(self.__sexp) == ffi.typeof("gcry_sexp_t"):
                return self.__sexp
            else:
                raise Exception

        if attr == 'car':
            #This method is used to return the car of a S-expression, which is the first element
            #of the S-expression. It is generally the type of the S-expression.
            return SExpression(lib.gcry_sexp_car(self.sexp))

        if attr == 'cdr':
            #Return the other part of the list (the list, minus the car)
            return SExpression(lib.gcry_sexp_cdr(self.sexp))

    def __setattr__(self, attr, value):
        if attr == 'sexp':
            # We want to setup the handle to an already existing in-memory SExpr
            self.__sexp = value
        super(SExpression, self).__setattr__(attr, value)

    def __len__(self):
        """
        Returns the len of the S-expression. It is defined as calling the sprint function but with
        a NULL buffer.
        """
        fmt = getattr(lib, u'GCRYSEXP_FMT_' + self.fmt)
        return lib.gcry_sexp_sprint(self.sexp, fmt, ffi.NULL, 0)

    def __repr__(self):
        """
        We need to print the S-expression in a format that can be used to be parsed
        into another S-expression.
        """
        fmt = getattr(lib, u'GCRYSEXP_FMT_' + self.fmt)
        bytes_out = ffi.new("char [{}]".format(len(self)))
        size = lib.gcry_sexp_sprint(self.sexp, fmt, bytes_out, len(self))
        return ffi.string(bytes_out).decode()

    def dump(self):
        """
        Dump the S-expression in a format suitable for libgcrypt debug mode
        """
        lib.gcry_sexp_dump(self.sexp)

    def __getitem__(self, key):
        """
        This is used to navigate through a S-expression, using token slice or indexes.
        """
        if isinstance(key, str):
            key = key.encode()
            sexp_match = lib.gcry_sexp_find_token(self.sexp, key, 0)
            if sexp_match != ffi.NULL:
                return SExpression(sexp_match)
            else:
                raise IndexError

        if isinstance(key, bytes):
            sexp_match = lib.gcry_sexp_find_token(self.sexp, key, 0)
            if sexp_match != ffi.NULL:
                return SExpression(sexp_match)
            else:
                raise IndexError

        if isinstance(key, int):
            sexp_match = lib.gcry_sexp_nth(self.sexp, key)
            if sexp_match != ffi.NULL:
                return SExpression(sexp_match)
            else:
                raise IndexError

        if isinstance(key, slice):
            start = key.start
            stop = key.stop
            if not (key.step == 1 or key.step == None):
                raise IndexError
            if stop > len(self) or start > len(self):
                raise IndexError
            fmt = u' %S' * (stop - start)
            fmt = u'({})'.format(fmt)
            fmt = fmt.encode()
            args = [SExpression(lib.gcry_sexp_nth(self.sexp, i)) for i in range(start, stop)]
            return SExpression(fmt, *args)

    def getstring(self, index):
        """
        This is used to get the string stored at index value in a SExpression.

        If the value can't be converted to a string or self[index] is another list, then
        we will return None
        """
        value = lib.gcry_sexp_nth_string(self.sexp, index)
        if value == ffi.NULL:
            return None
        return ffi.string(value)

    def getmpi(self, index, fmt='USG'):
        """
        This is used to get the mpi stored at index value in a SExpression

        If the value can't be converted to a MPI or self[index]  is another list, then
        we will return None
        """
        mpi = lib.gcry_sexp_nth_mpi(self.sexp, index, lib.GCRYMPI_FMT_USG)
        if mpi == ffi.NULL:
            return None
        # we need to pick between opaque and int MPI
        opaque = lib.gcry_mpi_get_flag(mpi, lib.GCRYMPI_FLAG_OPAQUE)
        if opaque == 1:
            result = MPIopaque()
        else:
            result = MPIint()
        result.mpi = mpi
        return result

    def extract(self, params, path=None):
        """
        Extract parameters from an S-expression using a list of parameters name. It works in a simialr way to getopts.
        We must first parse the params string, in order to allocate enough mpi to hold the data.
        The result will be a dict of MPI mapped to their param name.

        If path is precised we will search for parameters inside a sub S-epression
        """
        # Let's get the params first, and build MPI and a pointer list.
        match = re.compile(r"([+-/&]?\w{1}|'\w+')")
        results = match.findall(params)
        result = {}
        pointers = []
        for item in results:
            if item.startswith('-'):
                result[item[1:]] = MPIint()
                result[item[1:]].fmt = 'STD'
            else:
                result[item] = MPIint()
                result[item].fmt = 'USG'
            pointers += [ffi.new("gcry_mpi_t *", ffi.NULL)]

        # The poin-ters list must end with a NULL pointer.
        pointers += [ffi.NULL]
        if path == None:
            path = ffi.NULL

        error = ffi.cast("gcry_error_t", 0)
        error = lib.gcry_sexp_extract_param(self.sexp, path, params.encode(), *pointers)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)

        # Let's map the pointers back into MPI to have the correlation fixed
        i = 0
        for mpi in result:
            result[mpi].mpi = pointers[i][0]
            i+=1
        return result
