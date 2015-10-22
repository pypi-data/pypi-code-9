from configobj import ConfigObj, flatten_errors
from validate import Validator


_spec = '''\
[global]
persistent   = boolean(default=False)
base         = string
container_id = string(default=None)
user         = string(default=None)
sudo         = boolean(default=False)
on_activate  = force_list(min=0, default=None)
snapshots    = force_list(min=0, default=None)
profile      = string(default=None)

[directory]

[link]
'''


class Config(ConfigObj):
    def __init__(self, filename, validate=True, file_error=True):
        super(Config, self).__init__(
            filename, configspec=_spec.splitlines(), file_error=file_error)
        if validate:
            self.check()
        else:
            if 'global' not in self:
                self['global'] = {}
            if 'directory' not in self:
                self['directory'] = {}
            if 'link' not in self:
                self['link'] = {}

    def reload(self):
        super(Config, self).reload()
        self.check()

    def check(self):
        _validate(self)


def _validate(config):
    validator = Validator()
    valid = config.validate(validator, preserve_errors=True)

    if valid is True:
        return

    # format errors
    errors = []
    for sections, key, value in flatten_errors(config, valid):
        sections = [(('[' * (i + 1)) + section + (']' * (i + 1)))
                    for i, section in enumerate(sections)]
        path = ' -> '.join(sections + [key])

        if value is False:
            message = '%s is missing' % path
        else:
            message = '%s: %s' % (path, value)

        errors.append(message)

    raise ValueError('\n'.join(errors))

