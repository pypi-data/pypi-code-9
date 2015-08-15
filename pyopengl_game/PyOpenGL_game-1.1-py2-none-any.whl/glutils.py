from numpy import *


def dist(x, y):
    '''
    Calculate dist^2 between two points
    @param x: first point
    @param y: second point
    @return: distance^2
    '''
    r = 0.0
    for i in range(3):
        r += (x[i] - y[i]) ** 2
    return r


def comparer(pos):
    '''
    Return comparator for points
    @param pos: center position
    '''
    def _cmp(x, y):
        '''
        Compare points by distance relatively center position
        @param x: first point
        @param y: second point
        @return: result of comparison
        '''
        xr = dist(x.getPosition(), pos)
        yr = dist(y.getPosition(), pos)
        if xr < yr:
            return 1
        if xr > yr:
            return -1
        return 0
    return _cmp


def mul(a, b):
    '''
    Multiply two matrices represented in transposed form
    @param a: first matrix
    @param b: second matrix
    @return: a * b
    '''
    return transpose(dot(transpose(a), transpose(b)))


def mul_v(a, b):
    '''
    Multiply matrix represented in transposed form on vector
    @param a: matrix
    @param b: vector
    @return: matrix * vector
    '''
    return dot(transpose(a), b)


def v3_v4(a):
    '''
    Transform 3D vector to 4D vector
    @param a: 3D vector
    @return: 4D vector
    '''
    return array([a[0], a[1], a[2], 1.0], 'f')


def v4_v3(a):
    '''
    Transform 4D vector to 3D vector
    @param a: 4D vector
    @return: 3D vector
    '''
    return array([a[0] / a[3], a[1] / a[3], a[2] / a[3]], 'f')


def normalize(x):
    '''
    Normalize vector
    @param x: vector
    @return: normalized vector
    '''
    result = x.copy()
    norm = 0.0
    for i in result:
        norm += i * i
    if norm > 10.0 ** -5:
        for i in range(len(result)):
            result[i] /= sqrt(norm)
    return result


def translate(v):
    '''
    Calculate translation matrix
    @param v: translation vector
    @return: translation matrix
    '''
    result = identity(4, 'f')
    result[3][0] = v[0]
    result[3][1] = v[1]
    result[3][2] = v[2]
    return result


def rotate(angle, axis):
    '''
    Calculate rotation matrix
    @param angle: angle
    @param axis: axis
    @return: rotation matrix
    '''
    result = identity(4, 'f')
    u = normalize(axis)
    a = angle * pi / 180.0
    result[0][0] = cos(a) + u[0] * u[0] * (1 - cos(a))
    result[0][1] = u[1] * u[0] * (1 - cos(a)) + u[2] * sin(a)
    result[0][2] = u[2] * u[0] * (1 - cos(a)) - u[1] * sin(a)
    result[1][0] = u[0] * u[1] * (1 - cos(a)) - u[2] * sin(a)
    result[1][1] = cos(a) + u[1] * u[1] * (1 - cos(a))
    result[1][2] = u[2] * u[1] * (1 - cos(a)) + u[0] * sin(a)
    result[2][0] = u[0] * u[2] * (1 - cos(a)) + u[1] * sin(a)
    result[2][1] = u[1] * u[2] * (1 - cos(a)) - u[0] * sin(a)
    result[2][2] = cos(a) + u[2] * u[2] * (1 - cos(a))
    return result


def scale(s):
    '''
    Calculate scale matrix
    @param s: scale
    @return: scale matrix
    '''
    result = identity(4, 'f')
    result[0][0] = s[0]
    result[1][1] = s[1]
    result[2][2] = s[2]
    return result
