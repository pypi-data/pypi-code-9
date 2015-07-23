import numpy


def tojson(obj):
    if isinstance(obj, complex):
        return {'__class__': 'complex',
                '__value__': [obj.real, obj.imag]}

    if isinstance(obj, numpy.int64):
        return {'__class__': 'numpy.int64',
                '__value__': int(obj)}

    if isinstance(obj, numpy.complex128):
        return {'__class__': 'numpy.complex128',
                '__value__': [obj.real, obj.imag]}

    if isinstance(obj, numpy.ndarray):
        return {'__class__': 'numpy.ndarray',
                '__value__': list(obj)}

    raise TypeError(repr(obj) + 'is not JSON serializable')


def fromjson(json_obj):
    if '__class__' in json_obj:
        if json_obj['__class__'] == 'complex':
            temp = numpy.array(0+0j)
            temp.real = json_obj['__value__'][0]
            temp.imag = json_obj['__value__'][1]
            temp = numpy.complex128(temp)
            return complex(temp)

        if json_obj['__class__'] == 'numpy.int64':
            return numpy.int64(json_obj['__value__'])

        if json_obj['__class__'] == 'numpy.complex128':
            temp = numpy.array(0+0j)
            temp.real = json_obj['__value__'][0]
            temp.imag = json_obj['__value__'][1]
            return numpy.complex128(temp)

        if json_obj['__class__'] == 'numpy.ndarray':
            return numpy.asarray(json_obj['__value__'])

    return json_obj
