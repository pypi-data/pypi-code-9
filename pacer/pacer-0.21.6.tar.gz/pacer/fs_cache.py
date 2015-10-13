# encoding: utf-8

import glob
import hashlib
import inspect
import os
import weakref

import dill

import multiprocessing

from .std_logger import get_logger


def _fallback_save_function():
    ext = ".pickled"

    def save_function(what, path):
        with open(path, "wb") as fp:
            dill.dump(what, fp)
    return ext, save_function


def _fallback_load_function():

    def load_function(path):
        with open(path, "rb") as fp:
            return dill.load(fp)
    return load_function


def rel_path(p):
    """/abc/cde/xdf/x.table -> xdf/x.table"""
    return os.path.join(os.path.basename(os.path.split(p)[0]), os.path.split(p)[1])


class CacheItem(object):

    def __init__(self, meta, hash_code, tr):
        self.meta = meta.copy()
        self.hash_code = hash_code
        self.tr = tr
        self.rel_path = None
        self.loaded = False
        self.value = None

    def __str__(self):
        return "<CachedItem meta=%s rel_path=%s value=%r loaded=%s hash_code=%s>" % (
            self.meta, self.rel_path, self.value, self.loaded, self.hash_code)

    def load(self, cb):
        __, f_ext = os.path.splitext(self.rel_path)
        load_function = self.tr.lookup_load_function_for(f_ext)
        if load_function is None:
            load_function = _fallback_load_function()
        obj = load_function(os.path.join(cb.root_folder, self.rel_path))
        return obj


class AnnotatedItem(object):

    def __init__(self, value, **meta):
        self.value = value
        self.meta = meta


class CacheListItem(CacheItem):

    def __init__(self, meta, hash_code, tr):
        super(CacheListItem, self).__init__(meta, hash_code, tr)
        self.sub_items = []

    def __str__(self):
        return "<CacheListItem meta=%s rel_path=%s value=%r loaded=%s hash_code=%s>" % (
            self.meta, self.rel_path, self.value, self.loaded, self.hash_code)

    def save(self, what, path):
        self.sub_items = []
        for i, item in enumerate(what):
            ext, save_function = self.tr.lookup_ext_and_save_function_for(item)
            if ext is None or save_function is None:
                ext, save_function = _fallback_save_function()
            full_path = path + "_%d" % i + ext
            save_function(item, full_path)
            hash_code = self.tr.compute_hash(item)
            sub_item = CacheItem(self.meta, hash_code, self.tr)
            sub_item.rel_path = rel_path(full_path)
            self.sub_items.append(sub_item)
        self.rel_path = rel_path(path)

    def load(self, cb):
        items = []
        for p in glob.glob(os.path.join(cb.root_folder, self.rel_path + "_*.*")):
            __, f_ext = os.path.splitext(p)
            load_function = self.tr.lookup_load_function_for(f_ext)
            if load_function is None:
                load_function = _fallback_load_function()
            obj = load_function(p)
            items.append(obj)
        return items

    def __iter__(self):
        return iter(self.sub_items)


class DistributedTypeRegistry(object):

    def __init__(self):
        self._pickler = dill.dumps
        self._unpickler = dill.loads
        self.reset_handlers()

    def reset_handlers(self):
        self._type_handlers = list()

    def register_handler(self, type_, hash_data_source, file_extension, load_function,
                         save_function, info_getter):
        self._type_handlers.append((type_,
                                    self._pickler(hash_data_source),
                                    file_extension,
                                    self._pickler(load_function),
                                    self._pickler(save_function),
                                    self._pickler(info_getter),
                                    )
                                   )

    def lookup_load_function_for(self, ext):
        for (__, __, ext_i, load_function, __, __) in self._type_handlers:
            if ext == ext_i:
                return self._unpickler(load_function)
        return None

    def _lookup_for_type_of(self, obj):
        for row in self._type_handlers:
            if isinstance(obj, row[0]):
                return row
        nonf = self._pickler(None)
        return [None, nonf, None, nonf, nonf, nonf, nonf]

    def lookup_hash_data_extractor_for(self, key):
        return self._unpickler(self._lookup_for_type_of(key)[1])

    def lookup_ext_and_save_function_for(self, what):
        row = self._lookup_for_type_of(what)

        ext = row[2]
        save_function = self._unpickler(row[4])

        return ext, save_function

    def lookup_info_getter(self, what):
        row = self._lookup_for_type_of(what)
        return self._unpickler(row[5])

    def compute_hash(self, key):
        return self._compute_hash(key, set(), [])

    def _compute_hash(self, key, seen, keep):
        """we use see to handle recursive data strucutres, which might happen for example
        for namedtuples sometimes...
        further we keep local data in a list so that the id() calls are unique (we had
        different tuples here with same id because they were created temporarily and
        when recursing they were destroyed and other tuples occupied the same memory
        location, thus resulted in the same id)
        """
        if isinstance(key, CacheItem):
            return key.hash_code
        keep.append(key)
        extractor = self.lookup_hash_data_extractor_for(key)
        if extractor is not None:
            key = extractor(key)
            keep.append(key)
        if id(key) in seen and not isinstance(key, (int, float, bool, long, str, tuple)):
            # stop recursion here, return a placeholder which is unique for the item:
            # len() is a good choide because it correspondst to the current state of the
            # stack:
            data = "___memo_%s" % len(seen)
        else:
            seen.add(id(key))
            if isinstance(key, str):
                data = key
            elif isinstance(key, unicode):
                data = key.encode("utf-8")
            elif hasattr(key, "__dict__"):
                data = self._compute_hash(key.__dict__, seen, keep)
            elif isinstance(key, (bool, int, long, float,)):
                data = str(dill.dumps(key))
            elif key is None:
                data = "__None__"
            elif isinstance(key, (tuple, list)):
                data = []
                for item in key:
                    keep.append(item)
                    data.append(self._compute_hash(item, seen, keep))
                data = "".join(data)
            elif isinstance(key, set):
                data = []
                for item in sorted(key):
                    keep.append(item)
                    data.append(self._compute_hash(item, seen, keep))
                data = "".join(data)
            elif isinstance(key, dict):
                data = []
                for item in key.items():
                    keep.append(item[0])
                    keep.append(item[1])
                    keep.append(item)
                    data.append(self._compute_hash(item, seen, keep))
                data = "".join(data)
            else:
                raise Exception("can not compute hash for %r" % key)
            if not isinstance(data, basestring):
                raise RuntimeError("implementation error: data should be str, but is %s" % type(data))
        muncher = hashlib.sha1()
        muncher.update(data)
        hash_ = muncher.hexdigest()
        return hash_


class LocalTypeRegistry(DistributedTypeRegistry):

    def __init__(self):
        noop = lambda x: x
        self._pickler = noop
        self._unpickler = noop
        self.reset_handlers()


class _CacheBuilder(object):

    def __init__(self, root_folder=None):
        self.root_folder = root_folder
        self._logger = get_logger(self)

    def register_handler(self, *a, **kw):
        self.tr.register_handler(*a, **kw)

    def _setup_folder(self, function):
        folder = function.__name__
        if self.root_folder is not None:
            folder = os.path.join(self.root_folder, folder)
        return folder

    def __call__(self, function):
        # folder = self._setup_folder(function)
        cache, lock, counter = self._setup_cache_internals()

        clz = self._cache_function_class()
        c = clz(function, self.root_folder, lock, cache, counter, self.tr)

        return c

    def _cache_function_class(self):
        return _CachedFunction

    def create_dict(self):
        return dict()

    def remove_unused_entries(self):
        to_keep = set()
        for path in glob.glob(os.path.join(self.root_folder, "*", "__*")):
            to_keep.add(os.path.basename(path)[2:])
        for path in glob.glob(os.path.join(self.root_folder, "*", "*.cache_meta_file")):
            # we look for proper cache entries, we might have other files in the cache
            # folder...
            hash_value = os.path.splitext(os.path.basename(path))[0]
            folder = os.path.dirname(path)
            if hash_value not in to_keep:
                for path in glob.glob(os.path.join(folder, hash_value + "*")):
                    if path.endswith("_injected"): #  or path.endswith(".cache_meta_file"):
                        continue
                    try:
                        os.remove(path)
                    except IOError, e:
                        self._logger.error("could not remove %s: %s" % (path, e.message))

    def remove_use_markers(self):
        for path in glob.glob(os.path.join(self.root_folder, "*", "__*")):
            try:
                os.remove(path)
            except IOError, e:
                self._logger.error("could not remove %s: %s" % (path, e.message))


class CacheBuilder(_CacheBuilder):

    def __init__(self, root_folder=None):
        super(CacheBuilder, self).__init__(root_folder)
        self.tr = DistributedTypeRegistry()
        self._manager = multiprocessing.Manager()

        # shutdown manager if object is deleted, this has less impact to garbage collector
        # than implementing __del__:
        def on_die(ref, manager=self._manager, logger=get_logger()):
            logger.info("try to shutdown multiprocessings manager process")
            manager.shutdown()
            logger.info("finished shutdown multiprocessings manager process")
        self._del_ref = weakref.ref(self, on_die)

    def _setup_cache_internals(self):
        cache = self._manager.dict()
        lock = self._manager.Lock()
        counter = self._manager.Value('d', 0)
        return cache, lock, counter

    def __str__(self):
        return "<CacheBuilder(%s)>" % self.root_folder

    def create_dict(self):
        return self._manager.dict()


class LazyCacheBuilder(CacheBuilder):

    def _cache_function_class(self):
        return _LazyCachedFunction

    def __str__(self):
        return "<LazyCacheBuilder(%s)>" % self.root_folder


class LocalCounter(object):

    def __init__(self):
        self.value = 0


class NoOpContextManager(object):

    def __enter__(self, *a, **kw):
        pass

    __exit__ = __enter__


class LocalCacheBuilder(_CacheBuilder):

    """Cache which only resists in current process, can not be used with pacerd distributed
    computation capabilities ! Use CacheBuilder instead.
    """

    def __init__(self, root_folder=None):
        super(LocalCacheBuilder, self).__init__(root_folder)
        self.tr = LocalTypeRegistry()
        self._manager = None

    def _setup_cache_internals(self):
        cache = dict()
        lock = NoOpContextManager()
        counter = LocalCounter()
        #handlers = list(self._type_handlers)
        return cache, lock, counter  # , handlers

    def __str__(self):
        return "<LocalCacheBuilder(%s)>" % self.root_folder


class _CachedFunction(object):

    """ Instances of this class can be used to decorate function calls for caching their
    results, even if the functions are executed across different processes started by Python
    multiprocessing modules Pool class.

    The cache is backed up on disk, so that cache entries are persisted over different
    runs.
    """

    def __init__(self, function, root_folder, _lock, _cache, _counter, tr):

        self.function = function
        self.__name__ = function.__name__

        self._cache = _cache
        self._lock = _lock
        self._hit_counter = _counter

        self.root_folder = root_folder

        self.tr = tr

        self._logger = get_logger(self)
        self._setup_cache()
        self._arg_processor = None


    def folder(self):
        return os.path.join(self.root_folder, self.function.__name__)

    def __getstate__(self):
        dd = self.__dict__.copy()
        if "_logger" in dd:
            del dd["_logger"]
        return dd

    def register_handler(self, *a, **kw):
        self.tr.register_handler(*a, **kw)

    def __setstate__(self, dd):
        self.__dict__.update(dd)
        self._logger = get_logger(self)

    def get_number_of_hits(self):
        return self._hit_counter.value

    def set_cache_key_preprocessor(self, **kw):
        self._arg_processor = kw

    def _setup_cache(self):
        folder = os.path.join(self.root_folder, self.function.__name__)
        if not os.path.exists(folder):
            os.makedirs(folder)
        for file_name in os.listdir(folder):
            path = os.path.join(folder, file_name)
            stem, ext = os.path.splitext(file_name)
            if ext == ".cache_meta_file":
                with open(path, "rb") as fp:
                    item = dill.load(fp)
                    self._cache[stem] = item

    def clear(self):
        self._cache.clear()

    def _contains(self, hash_code):
        return hash_code in self._cache.keys()

    def _get(self, hash_code):
        item = self._cache[hash_code]
        if not item.loaded:
            value = item.load(self)
            item.value = value
            item.loaded = True
        self._cache[hash_code] = item
        return item.value

    def _put(self, name, hash_code_args, result, injected=False):
        item = self._store(name, result, hash_code_args, injected)
        self._cache[hash_code_args] = item
        self._set_use_marker(hash_code_args)
        return item

    def inject_result(self, hash_code, value):
        for hash_code_args, ci in self._cache.items():
            if ci.hash_code == hash_code:
                self._put("injected", hash_code_args, value, injected=True)

    def remove_injected_result(self, hash_code):
        for hash_code_args, ci in self._cache.items():
            if ci.hash_code == hash_code:
                if ci.rel_path.endswith("_injected"):
                    os.remove(os.path.join(self.root_folder, ci.rel_path))
                    new_rel_path = ci.rel_path.rsplit("_", 1)[0]
                    new_path = os.path.join(self.root_folder, new_rel_path)
                    if os.path.exists(new_path):
                        ci.rel_path = new_rel_path
                        self._write_meta(hash_code_args, ci)
                        # self._cache is not a pure python dict, we have to write back:
                        self._cache[hash_code_args] = ci
                    else:
                        del self._cache[hash_code_args]

    def _store(self, name, result, hash_code_args, injected=False):

        hash_code_result = self.tr.compute_hash(result)
        meta = dict(name=name)
        if isinstance(result, AnnotatedItem):
            extra = result.meta
            result = result.value
            if extra is not None:
                meta.update(extra)

        if isinstance(result, list):
            item = CacheListItem(meta, hash_code_result, self.tr)
            save_function = item.save
            ext = ""
        else:
            item = CacheItem(meta, hash_code_result, self.tr)
            ext, save_function = self.tr.lookup_ext_and_save_function_for(result)
            if ext is None or save_function is None:
                ext, save_function = _fallback_save_function()
        path = os.path.join(self.root_folder, self.function.__name__, hash_code_args + ext)

        if injected:
            path += "_injected"
        item.rel_path = rel_path(path)

        if injected or not os.path.exists(path):
            save_function(result, path)
            self._logger.info("stored %s" % path)
        else:
            self._logger.info("no need to store item to %s" % path)

        self._write_meta(hash_code_args, item)
        return item

    def _write_meta(self, hash_code_args, item):
        path = os.path.join(self.root_folder, self.function.__name__, hash_code_args + ".cache_meta_file")
        with open(path, "wb") as fp:
            dill.dump(item, fp)
        return item

    def _get_names(self, args):
        for arg in args:
            if isinstance(arg, CacheItem):
                yield arg.name
            else:
                getter = self.tr.lookup_info_getter(arg)
                if getter is not None:
                    yield getter(arg)

    def _setup_args(self, args):
        if self._arg_processor is None:
            return args
        arg_names = inspect.getargspec(self.function).args
        result = []
        for arg, name in zip(args, arg_names):
            if not isinstance(arg, CacheItem):
                if name in self._arg_processor:
                    arg_processor = self._arg_processor.get(name)
                    if hasattr(arg_processor, "__call__"):
                        arg = arg_processor(arg)
                    else:
                        arg = arg_processor
            result.append(arg)
        return result

    def cached_call(self, args, kw):
        all_args = list(args) + list(sorted(kw.items()))
        try:
            args_for_hash = self._setup_args(all_args)
            hash_code_args = self.tr.compute_hash(args_for_hash)
        except RuntimeError:
            raise Exception("could not compute hash for %r. maybe you should register your own "
                            "handler" % (all_args,))
        if self._contains(hash_code_args):
            with self._lock:
                self._hit_counter.value += 1
            self._logger.info("cache hit for %s" % hash_code_args)
            ci = self._get(hash_code_args)
            self._set_use_marker(hash_code_args)
            return ci, ci

        args = self.resolve_inputs(args)
        result = self.function(*args, **kw)

        self._logger.info("new result for %s" % hash_code_args)
        name = "--".join(a for a in self._get_names(args) if a is not None)
        if name == "":
            name = None
        item = self._put(name, hash_code_args, result)
        return result, item

    def _set_use_marker(self, hash_code):
        sub_folder = os.path.join(self.root_folder, self.function.__name__)
        marker_path = os.path.join(sub_folder, "__" + hash_code)
        try:
            with open(marker_path, "w") as fp:
                pass
        except IOError, e:
            self._logger.error("could not write to %s: %s" % (marker_path, e.message))
            raise


    def __call__(self, *args, **kw):
        result, item = self.cached_call(args, kw)
        return result

    def resolve_inputs(self, i):
        return i

    def __str__(self):
        return "<_CachedFunction(%s)>" % self.function.__name__


class _LazyCachedFunction(_CachedFunction):

    def _get(self, hash_code):
        item = self._cache[hash_code]
        # item ist multiple + modues is "beak lists" ?
        # aufliösen zu liste von cacheitems
        return item

    def __call__(self, *args, **kw):
        result, item = self.cached_call(args, kw)
        return item

    def __str__(self):
        return "<_LazyCachedFunction(%s)>" % self.function.__name__

    def resolve_inputs(self, args):
        if isinstance(args, (list, tuple)):
            loaded = [a.load(self) if isinstance(a, CacheItem) else self.resolve_inputs(a) for a in args]
            if isinstance(args, (tuple,)):
                loaded = tuple(loaded)
            return loaded
        if isinstance(args, CacheItem):
            return args.load(self)
        return args

