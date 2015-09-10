import inspect


class Formula(object):
    u"""
    formulas registry
    """
    __ARGS_KEY__ = 0
    __SRC_KEY__ = 1
    __CALL_KEY__ = 2

    def __init__(self):
        self.__num_registry = {}
        self.__fn_registry = {}
        self.__param_registry = {}

    def __call__(self, key=None):
        if isinstance(key, int):
            if key not in self.__num_registry:
                return self.__decorator(key)
            else:
                return self.__num_registry[key]
        elif isinstance(key, str):
            try:
                return self.get_param(key)
            except KeyError:
                try:
                    return self.get_fn_by_name(key)
                except KeyError:
                    return None
        elif isinstance(key, dict):
            self.__param_registry.update(key)
        elif not key:
            return self.__decorator()

    def __decorator(self, num=None):
        def wrap(fn):
            def wrapped_fn(*args, **kwargs):
                self.__param_registry[fn.__name__] = fn(*args, **kwargs)
                self.__param_registry.update(
                    dict(
                        zip(
                            self.__fn_registry[fn.__name__][Formula.__ARGS_KEY__][1], args
                        )
                    )
                )

                return self.__param_registry[fn.__name__]

            self.__fn_registry[fn.__name__] = (
                ('args', inspect.getargspec(fn).args),
                ('src', inspect.getsourcelines(fn)),
                ('call', wrapped_fn),
            )

            if num:
                self.__num_registry[num] = self.__fn_registry[fn.__name__][Formula.__CALL_KEY__][1]

            return self.__fn_registry[fn.__name__][Formula.__CALL_KEY__][1]
        return wrap

    def get_param(self, param):
        return self.__param_registry[param]

    def get_params(self):
        return self.__param_registry

    def get_fns(self):
        return self.__fn_registry

    def get_nums(self):
        return self.__num_registry

    def get_fn_by_name(self, fn_name):
        return self.__fn_registry[fn_name]

    def __str__(self):
        return str({
            'num_registry': self.__num_registry,
            'fn_registry': self.__fn_registry,
            'param_registry': self.__param_registry
        })
