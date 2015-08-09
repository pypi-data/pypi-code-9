#The MIT License (MIT)

#Copyright (c) 2015 Peter Row

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


import json
from collections import defaultdict,namedtuple
MAX_ARRAY = 1000

def nim_cdef(ffi,output_f):
    s=json.load(open(output_f))
    ffi.cdef(base_type_cdef())
    funcTable = converted_funcTable(s['funcTable'])
    classes = s['classnameFromInt']
    
    for k in list(funcTable):
        ffi.cdef(funcTable[k].to_cdef(k))
    
    for k in classes:
        ffi.cdef(class_to_cdef(k))

def nim_wrap(ffi, ffi_lib, output_f):
    s=json.load(open(output_f))
    funcTable = converted_funcTable(s['funcTable'])
    classes = s['classnameFromInt']
    methTable = s['methTable']
    class_to_meth = {}
    for (k,v) in methTable.items():
        if not v in class_to_meth:
            class_to_meth[v] = []
        class_to_meth[v].append(k)
    
    python_classes = []
    funcs= {}
    
    convert_to_nim =  get_convert_to_nim(ffi)
    convert_from_nim = get_convert_from_nim(ffi,python_classes)
    
    for k in funcTable:
        c_func = getattr(ffi_lib,k.replace('.','__'))
        if k in methTable: continue
        funcs[k] = get_func(ffi,c_func,funcTable[k],convert_to_nim,convert_from_nim)
    
    # make classes:
    for k in classes:
        mod_name,class_name = k.rsplit('.',1)
        del_meth = getattr(ffi_lib,'del__'+k.replace('.','__'))
        methods = [("_del",del_meth)]
        for meth in class_to_meth.get(k,[]):
            c_meth = getattr(ffi_lib,meth.replace('.','__'))
            meth_func = get_func(ffi,c_meth,funcTable[meth],convert_to_nim,convert_from_nim)
            methods.append((meth.rsplit('.',1)[-1],meth_func))
        klass = type(str(class_name), (NimBase,),dict(methods))
        python_classes.append(klass)
    
    import sys,imp
    modules = {}
    for k in funcs:
        mod_name,func_name =k.rsplit('.',1)
        if not mod_name in modules:
            module = imp.new_module("_"+mod_name)
            module.__file__ = mod_name+'.nim'
            modules[mod_name] = module
        module = modules[mod_name]
        setattr(module,func_name,funcs[k])
    sys.meta_path.append(FFIImporter(modules))

class FFIImporter(object):
    def __init__(self,modules):
        import imp
        for mod_name in list(modules):
            if not '.' in mod_name: continue
            parent_name,mod = mod_name.rsplit('.',1)
            while parent_name:
                if parent_name in modules:
                    parent_mod = modules[parent_name]
                else:
                    parent_mod = imp.new_module("_"+parent_name)
                    parent_mod.__path__="_"+parent_name
                    modules[parent_name]=parent_mod
                setattr(parent_mod,mod,modules[mod_name])
                mod_name = parent_name
                if not '.' in parent_name: break
                parent_name,mod = parent_name.rsplit('.',1)
        self.modules = modules
    
    def find_module(self, fullname, path=None):
        if fullname.startswith('_'):
            if fullname[1:] in self.modules:
                return self
        
    def load_module(self, fullname):
        import sys
        if fullname in sys.modules:
            return sys.modules[fullname]
        return self.modules[fullname[1:]]


def converted_funcTable(funcTable):
    result = {}
    for k in sorted(list(funcTable)):
        row = funcTable[k]
        resultSpec = ArgSpec(*row[0])
        paramSpecs = [ParamSpec(a[0],ArgSpec(*a[1])) for a in row[1]]
        result[k] = FuncSig(resultSpec,paramSpecs)
    return result

class NimBase(object):
    __slots__=['_cptr']
    def __init__(self,cptr):
        self._cptr = cptr
    
    def __del__(self):
        self._del(self._cptr[0])

nimTypes = (aRef,aInt,aFloat,aStr) = ("aRef","aInt","aFloat","aStr")
wrapTypes =  (wRaw,wSafe,wArray,wSafeSeq) = ("wRaw","wSafe","wArray","wSafeSeq")

class ArgSpec(namedtuple('ArgSpec', 'wrapType argType')):
    def to_arg(self):
        return "%s_%s"%(self)

class ParamSpec(namedtuple('ParamSpec', 'name argSpec')):
    def to_arg(self):
        if self.argSpec.wrapType==wArray:
            return "%s_%s"%(self.argSpec)
        return self.argSpec.to_arg()

class FuncSig(namedtuple('FuncSig', 'resultSpec paramSpecs')):
    def to_cdef(self,classname):
        """This is horrible code, that tries to match how nim declares func declarations.
        
        It was developed by trial, error, and reading nim's generated header files."""
        if self.resultSpec.argType == aRef or self.resultSpec.wrapType == wSafeSeq:
            args = [a.to_arg() for a in self.paramSpecs]+[self.resultSpec.to_arg()+"*"]
            arg_string = ', '.join(args)
            return "void %s(%s);"%(classname.replace('.','__'),arg_string)
        else:
            arg_string = ', '.join([a.to_arg() for a in self.paramSpecs])
            return "%s %s(%s);"%(self.resultSpec.to_arg(),classname.replace('.','__'),arg_string)

def get_func(ffi,c_func, funcSig,convert_to_nim,convert_from_nim):
    resultSpec = funcSig.resultSpec
    paramSpecs = funcSig.paramSpecs
    if resultSpec.argType == aRef or resultSpec.wrapType == wSafeSeq:
        def f_with_ref(*args):
            res_ptr = ffi.new(resultSpec.to_arg()+"*")
            c_func(*(args+(res_ptr,)))
            return res_ptr
    else:
        f_with_ref = c_func
    converters = [convert_to_nim.get(param.argSpec,None) for param in paramSpecs]
    res_converter = convert_from_nim.get(resultSpec,None)
    if [c for c in converters if c]:
        if res_converter:
            def f_arg_converted(*args):
                res = f_with_ref(*[a if not c else c(a) for (a,c) in zip(args,converters)])
                return res_converter(res)
        else:
            def f_arg_converted(*args):
                return f_with_ref(*[a if not c else c(a) for (a,c) in zip(args,converters)])
    else:
        if res_converter:
            def f_arg_converted(*args):
                return res_converter(f_with_ref(*args))
        else:
            f_arg_converted = f_with_ref
    return f_arg_converted

def class_to_cdef(class_name):
    return 'void del__%s(wRaw_aRef);'%class_name.replace('.','__')

def get_convert_to_nim(ffi):
    convert_to_nim = {}

    def to_nim(wrapType,nimType):
        assert wrapType in wrapTypes
        assert nimType in nimTypes
        def wrapper(f):
            convert_to_nim[(wrapType,nimType)]=f
        return wrapper

    @to_nim(wRaw,aStr)
    def f(s):
        return s.encode('utf8')

    @to_nim(wArray,aStr)
    def f(s_list):
        if len(s_list)>MAX_ARRAY: raise ValueError("too big!")
        return ffi.new("wArray_aStr",(len(s_list),[ffi.new("char[]",s.encode('utf8')) for s in s_list])) 

    @to_nim(wArray,aInt)
    def f(i_list):
        if len(i_list)>MAX_ARRAY: raise ValueError("too big!")
        return ffi.new("wArray_aInt",(len(i_list),i_list)) 

    @to_nim(wArray,aFloat)
    def f(f_list):
        if len(f_list)>MAX_ARRAY: raise ValueError("too big!")
        return ffi.new("wArray_aFloat",(len(f_list),f_list)) 

    @to_nim(wRaw,aRef)
    def f(obj):
        return obj._cptr[0]

    @to_nim(wArray,aRef)
    def f(obj_list):
        if len(obj_list)>MAX_ARRAY: raise ValueError("too big!")
        return ffi.new("wArray_aRef",(len(obj_list),[o._cptr[0] for o in obj_list])) 
    return convert_to_nim
    
def get_convert_from_nim(ffi,classes):
    """
    There's a lot of code here.
    
    Should it be refactored?
    
    ["Get_Safe", "Get_Raw", "GetSafeSeq"] x ["Int", "Str", "Ref"]
    
    9 methods.if unfactored (Float just copies int)
    
    6 methods if factored.
    
    Not a world-beating savings, and it will be more complex to code, 
    and the extra function call will hurt performance.
    
    I could also write templates to eval the functions, re-write in C,
    maybe create custom eval'd functions for every single function I want to wrap ...
    
    Thats a Todo.
    """
    convert_from_nim = {}
    def from_nim(wrapType,nimType):
        assert wrapType in wrapTypes
        assert nimType in nimTypes
        def wrapper(f):
            convert_from_nim[(wrapType,nimType)]=f
        return wrapper
    
    # don't forget
    nimTypes = (aRef,aInt,aFloat,aStr)
    wrapTypes =  (wRaw,wSafe,wArray,wSafeSeq)
    
    def handle_error(v):
        raise ValueError(ffi.string(v.msg).decode('utf8'))
    
    @from_nim(wRaw,aStr)
    def f(s):
        return ffi.string(s).decode('utf8')
    
    @from_nim(wSafe,aStr)
    def f(s):
        if s.has_err: handle_error(s)
        return ffi.string(s.result).decode('utf8')
    
    @from_nim(wSafeSeq,aStr)
    def f(safe_seq_ptr):
        safe_seq = safe_seq_ptr[0]
        if safe_seq.has_err: handle_error(safe_seq)
        seq = safe_seq.result[0]
        result = []
        for i in range(seq.Sup.len):
            result.append(ffi.string(seq.result[i]).decode('utf8'))
        return result

    @from_nim(wSafe,aInt)
    def f(s):
        if s.has_err: handle_error(s)
        return s.result
    
    @from_nim(wSafeSeq,aInt)
    def f(safe_seq_ptr):
        safe_seq = safe_seq_ptr[0]
        if safe_seq.has_err: handle_error(safe_seq)
        seq = safe_seq.result
        result = []
        for i in range(seq.Sup.len):
            result.append(seq.result[i])
        return result
    
    for t in (wSafe,wSafeSeq):
        convert_from_nim[t,aFloat]=convert_from_nim[t,aInt]
    
    @from_nim(wRaw,aRef)
    def f(s):
        return classes[s.nim_class](s)
    
    @from_nim(wSafe,aRef)
    def f(s):
        if s.has_err: handle_error(s)
        return classes[s.result.nim_class](s.result)
    
    @from_nim(wSafeSeq,aRef)
    def f(safe_seq_ptr):
        safe_seq = safe_seq_ptr[0]
        if safe_seq.has_err: handle_error(safe_seq)
        seq = safe_seq.result[0]
        result = []
        for i in range(seq.Sup.len):
            ref = seq.result[i]
            result.append(classes[ref.nim_class](ffi.new("wRaw_aRef*",ref)))
        return result
    return convert_from_nim

def base_type_cdef():
    cdef = """
void NimMain();
typedef long NI;
typedef double NF;
typedef bool NIM_BOOL;
typedef char * NS;

typedef NI wRaw_aInt;
typedef NF wRaw_aFloat;
typedef NS wRaw_aStr;

typedef struct{
    NI nim_class;
    void * result;
} wRaw_aRef;

typedef struct {
NI len;
NI reserved;
} TGenericSeq;"""
    for t in nimTypes:
        cdef +=r"""
typedef struct <
    NIM_BOOL has_err;
    wRaw_aStr msg;
    wRaw_{t} result;
> wSafe_{t};

typedef struct <
    TGenericSeq Sup;
    wRaw_{t} result[];
> wSeq_{t};

typedef struct <
    NIM_BOOL has_err;
    wRaw_aStr msg;
    wSeq_{t} * result;
> wSafeSeq_{t};

typedef struct <
    NI len;
    wRaw_{t} data[1000];
> wArray_{t}_inner;

typedef wArray_{t}_inner* wArray_{t};
""".format(t=t).replace('>','}').replace('<','{')
    return cdef


def get_func_module(classname):
    return '.'.join(classname.split('.')[:-1])

class fakemodule(object):
    pass
