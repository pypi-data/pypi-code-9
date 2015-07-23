import json
import os

from cfnparams.stack import ResolutionError


class CLIParams(object):
    def __init__(self, param_str):
        self.param_str = param_str

    @classmethod
    def supports_source(cls, source):
        return source.startswith('ParameterKey=')

    def parse(self, resolver):
        strip_len = len('ParameterKey=')
        key, value = self.param_str[strip_len:].split(',ParameterValue=', 1)
        return {key: value}

    def dependencies(self):
        return set()


class JSONParams(object):
    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def supports_source(cls, source):
        return source.endswith('.json')

    def parse(self, resolver):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'rb') as f:
            params = json.loads(f.read())
        return {p['ParameterKey']: p['ParameterValue'] for p in params}

    def dependencies(self):
        return set()

    def write(self, params, use_previous_value):
        transform = [
            {
                "ParameterKey": key,
                "ParameterValue": value,
                "UsePreviousValue": use_previous_value
            }
            for key, value in params.iteritems()
        ]

        with open(self.filename, 'wb') as f:
            f.write(json.dumps(
                transform,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            ))


class PythonParams(object):
    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def supports_source(cls, source):
        return source.endswith('.py')

    def parse(self, resolver):
        _globals = {}
        _locals = {
            'GetOutput': (lambda stack, key: resolver(stack, key)),
        }
        return self.eval_py(_globals, _locals)

    def dependencies(self):
        stacks = set()

        _globals = {}
        _locals = {
            'GetOutput': (lambda stack, _: stacks.add(stack))
        }

        self.eval_py(_globals, _locals)
        return stacks

    def eval_py(self, _globals, _locals):
        """
        Evaluates a file containing a Python params dictionary.
        """
        if not os.path.exists(self.filename):
            return {}

        with open(self.filename, 'rb') as f:
            try:
                params = eval(f.read(), _globals, _locals)
            except NameError as e:
                raise Exception(
                    'Failed to evaluate parameters: {}'
                    .format(str(e))
                )
            except ResolutionError as e:
                raise Exception(
                    'GetOutput could not resolve: {}.\n{}'
                    .format(list(e.args), str(e))
                )

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
        if src.startswith(cls.FILE_PREFIX):
            src = os.path.abspath(src[len(cls.FILE_PREFIX):])

        for source_cls in cls.sources:
            if source_cls.supports_source(src):
                return source_cls(src)

        raise UnsupportedParameterSource(src)


class UnsupportedParameterSource(Exception):
    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return 'Unsupported Parameter Source "{}"'.format(self.src)
