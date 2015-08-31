import scipy

def condition(point):
    l = len(point.param['free'])
    a = len(point.param['artificial'])

    result = {}
    result['row'] = point.secant['u']
    result['d'] = scipy.zeros((l+a,), scipy.float64)
    result['d'][l-1] = point.secant['lambd'][point.param['free']]
    result['res'] = 0
    return result
        
