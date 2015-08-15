from validators import chainable, spec_validator

CONTENT_TYPES = ['html', 'video', 'audio', 'image', 'generic', 'app']


def content_type(TYPE_SPECS):
    @chainable
    def validator(v):
        errors = {}
        for key in v:
            value = v[key]
            key_string = 'content.{}'.format(key)

            if key not in TYPE_SPECS:
                errors['content'] = {
                    key: ValueError('content type must be one of '
                                   '{}'.format(CONTENT_TYPES), 'content_type')}
            elif type(value) != dict:
                errors['content'] = {
                    key: ValueError('{} must be a '
                                    'dict'.format(key), 'content_type')}
            else:
                VALIDATOR = spec_validator(
                    TYPE_SPECS[key], key=lambda k: lambda obj: obj.get(k))
                e = VALIDATOR(value)
                if e:
                    errors[key_string] = e
                elif key == 'audio':
                    i = 0
                    spec = TYPE_SPECS['audio.playlist']
                    VALIDATOR = spec_validator(
                        spec, key=lambda k: lambda obj: obj.get(k))
                    for item in value['playlist']:
                        i += 1
                        e = VALIDATOR(item)
                        if e:
                            s = key_string + '.' + str(i)
                            errors[s] = e
                elif key == 'image':
                    i = 0
                    spec = TYPE_SPECS['image.album']
                    VALIDATOR = spec_validator(
                        spec, key=lambda k: lambda obj: obj.get(k))
                    for item in value['album']:
                        i += 1
                        e = VALIDATOR(item)
                        if e:
                            s = key_string + '.' + str(i)
                            errors[s] = e
        final_set = []
        if errors:
            for key in errors:
                set = []
                for k in errors[key]:
                    key_string = '.'.join([key, k])
                    msg = errors[key][k].args[0]
                    string = '{}: {}'.format(key_string, msg)
                    set.append(string)
                final_set.append('\n'.join(set))
            error_string = '\n' + '\n'.join(final_set)
            raise ValueError(error_string, 'content_type')
        return v
    return validator
