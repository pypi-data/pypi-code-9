import json
import os

from cfnparams.resolution import ResolutionError


class CLIParams(object):
    def __init__(self, param_str):
        self.param_str = param_str

    @classmethod
    def supports_source(cls, source):
        return source.startswith('ParameterKey=')

    def parse(self, resolver=None):
        strip_len = len('ParameterKey=')
        key, value = self.param_str[strip_len:].split(',ParameterValue=', 1)
        return {key: value}


class JSONParams(object):
    def __init__(self, json_str):
        if json_str is None:
            json_str = '{}'
        self.params = json.loads(json_str)

    @classmethod
    def supports_source(cls, source):
        return source.startswith('file://') and source.endswith('.json')

    def parse(self, resolver=None):
        return {p['ParameterKey']: p['ParameterValue'] for p in self.params}

    def write(self, use_previous_value):
        transform = [
            {
                "ParameterKey": key,
                "ParameterValue": value,
                "UsePreviousValue": use_previous_value
            }
            for key, value in self.params.iteritems()
        ]

        return json.dumps(
            transform,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )


class PythonParams(object):
    def __init__(self, py_str):
        if py_str is None:
            py_str = '{}'
        self.script = py_str

    @classmethod
    def supports_source(cls, source):
        return source.startswith('file://') and source.endswith('.py')

    def parse(self, resolver):
        _globals = {}
        _locals = {
            'GetOutput': (lambda stack, key: resolver(stack, key)),
        }
        return self.eval_py(_globals, _locals)

    def eval_py(self, _globals, _locals):
        """
        Evaluates a file containing a Python params dictionary.
        """
        try:
            params = eval(self.script, _globals, _locals)
        except NameError as e:
            raise Exception(
                'Failed to evaluate parameters: {}'
                .format(str(e))
            )
        except ResolutionError as e:
            raise Exception('GetOutput: {}'.format(str(e)))

        return params


class ParamsFactory(object):
    sources = [
        CLIParams,
        JSONParams,
        PythonParams,
    ]

    FILE_PREFIX = 'file://'

    @classmethod
    def new(cls, src):
        content = None
        if src.startswith(cls.FILE_PREFIX):
            filename = os.path.abspath(src[len(cls.FILE_PREFIX):])
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    content = f.read()
        else:
            content = src

        for source_cls in cls.sources:
            if source_cls.supports_source(src):
                return source_cls(content)

        raise UnsupportedParameterSource(src)


class UnsupportedParameterSource(Exception):
    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return 'Unsupported Parameter Source "{}"'.format(self.src)
