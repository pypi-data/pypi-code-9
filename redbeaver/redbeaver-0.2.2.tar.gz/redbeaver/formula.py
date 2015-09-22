import inspect


class Formula(object):
    u"""
    formulas registry
    """
    __ARGS_KEY__ = 0
    __SRC_KEY__ = 1
    __CALL_KEY__ = 2

    def __init__(self):
        self._num_registry = {}
        self._fn_registry = {}
        self._param_registry = {}

    def __call__(self, key=None):
        if isinstance(key, int):
            if key not in self._num_registry:
                return self.__decorator(key)
            else:
                return self._num_registry[key]
        elif isinstance(key, str):
            return self.get_param_or_fn(key)
        elif isinstance(key, dict):
            self._update_param_registry(key)
        elif not key:
            return self.__decorator()

    def __decorator(self, num=None):
        def wrap(fn):
            return self._wrap_body(fn, num)
        return wrap

    def _update_fn_registry(self, fn, wrapped_fn):
        self._fn_registry[fn.__name__] = (
            ('args', inspect.getargspec(fn).args),
            ('src', inspect.getsourcelines(fn)),
            ('call', wrapped_fn),
        )

    def _wrap_body(self, fn, num):
        def wrapped_fn(*args, **kwargs):
            return self._wrapped_fn_body(fn, *args, **kwargs)

        self._update_fn_registry(fn, wrapped_fn)

        if num:
            self._update_num_registry(num, fn)

        return self._get_or_call_fn(fn.__name__)

    def _wrapped_fn_body(self, fn, *args, **kwargs):
        self._param_registry[fn.__name__] = fn(*args, **kwargs)
        self._update_param_registry(
            dict(
                zip(
                    self._get_fn_args(fn.__name__), args
                )
            )
        )

        return self.get_param(fn.__name__)

    def _get_fn_args(self, fn_name):
        return self._fn_registry[fn_name][Formula.__ARGS_KEY__][1]

    def _get_or_call_fn(self, fn_name, *params):
        fn = self._fn_registry[fn_name][Formula.__CALL_KEY__][1]

        if params:
            return fn(*params)

        return fn

    def _get_fn_src(self, fn_name):
        return self._fn_registry[fn_name][Formula.__SRC_KEY__][1]

    def _update_param_registry(self, new_params):
        self._param_registry.update(new_params)

    def _update_num_registry(self, num, fn):
        self._num_registry[num] = self._get_or_call_fn(fn.__name__)

    def get_param(self, param):
        return self._param_registry[param]

    def get_params(self):
        return self._param_registry

    def get_fns(self):
        return self._fn_registry

    def get_nums(self):
        return self._num_registry

    def get_fn_by_name(self, fn_name):
        return self._fn_registry[fn_name]

    def get_param_or_fn(self, key):
        try:
            return self.get_param(key)
        except KeyError:
            try:
                return self.get_fn_by_name(key)
            except KeyError:
                return None

    def reset_params(self):
        self._param_registry = {}

    def __str__(self):
        return str({
            'num_registry': self._num_registry,
            'fn_registry': self._fn_registry,
            'param_registry': self._param_registry
        })
