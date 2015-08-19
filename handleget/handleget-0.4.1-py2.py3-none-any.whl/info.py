_version = '0.4.1'

class info(object):
    # because click handles the wrapping, the strings are just one single line
    verbose_cmd =      'Turn on verbose output'

    service_cmd =      'List of services, deliminated by a comma. For '+\
                       'example: --services gi,go,twitter'

    conf_cmd =         'Path to config yaml file. Defaults to '+\
                       '<install_dir>/data/config.yml'

    strip_cmd =        'If enabled, all usernames will be filtered in order'+\
                       'to remove invalid characters, as defined by '+\
                       '--char-pattern'

    char_pattern_cmd = 'Overrides the standard default character regular '+\
                       'expression. Documentation for defining these is ' +\
                       'located in /doc/reference.md'
