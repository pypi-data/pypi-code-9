from redbeaver.exceptions import InfiniteLoopError


class Calc(object):
    u"""
    formula calculation
    """

    def __init__(self, formula):
        self.formula = formula

    def __call__(self, fn_name, iterate_param=None):
        self.__tree = []
        self.__iterate_params = [iterate_param] or iterate_param

        return self.__calc(fn_name)

    def __calc(self, fn_name):
        u"""
        calculation
        """
        if fn_name in self.__tree:
            raise InfiniteLoopError('Infinite loop on "%s" arg.\nCalc tree: %s' % (fn_name, self.__tree))
        else:
            self.__tree.append(fn_name)

        if fn_name in self.formula.get_fns():
            return self.__calc_fn(fn_name, *self.__calc_params(fn_name))
        else:
            raise Exception('Undefined fn: %s' % (fn_name,))

    def __calc_params(self, fn_name):
        u"""
        function params mapping
        """
        params = {}
        iterate_param = None

        for arg in self.formula.get_fn_by_name(fn_name)[self.formula.__ARGS_KEY__][1]:
            if arg in self.formula.get_params():
                params[arg] = self.formula.get_param(arg)
            else:
                params[arg] = self.__calc(arg)

            if arg in self.__iterate_params:
                iterate_param = arg
                self.__iterate_params.append(fn_name)

        return params, iterate_param

    def __calc_fn(self, fn_name, params, iterate_param):
        u"""
        function calculation
        """
        if iterate_param:
            try:
                res = []
                for arg in params[iterate_param]:
                    params[iterate_param] = arg
                    res.append(self.formula.get_fn_by_name(fn_name)[self.formula.__CALL_KEY__][1](**params))
            except TypeError:
                raise TypeError('iterate_param_ %s=%s is not iterable' % (iterate_param, params[iterate_param]))
        else:
            res = self.formula.get_fn_by_name(fn_name)[self.formula.__CALL_KEY__][1](**params)

        self.formula({fn_name: res})

        return res

    def get_tree(self):
        return self.__tree

    def get_iterate_params(self):
        return self.__iterate_params
