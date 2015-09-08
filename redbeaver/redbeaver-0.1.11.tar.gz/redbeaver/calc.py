from redbeaver.exceptions import InfiniteLoopError


def calc(fn_name, eq):
    if not hasattr(calc, 'tree'):
        calc.tree = []

    if fn_name in calc.tree:
        raise InfiniteLoopError('Infinite loop on "%s" arg.\nCalc tree: %s' % (fn_name, calc.tree))
    else:
        calc.tree.append(fn_name)

    if fn_name in eq.eq_registry:
        params = {}
        for arg in eq.eq_registry[fn_name]['args']:
            if arg in eq.params:
                params[arg] = eq.params.get(arg)
            else:
                params[arg] = calc(arg, eq)

        res = eq.eq_registry[fn_name]['fn'](**params)
    else:
        raise Exception('Undefined fn: %s' % (fn_name,))

    return res
