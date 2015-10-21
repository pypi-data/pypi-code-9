from __future__ import (unicode_literals, division,
                        absolute_import, print_function)


import json


def get_json(module):
    from reggae.reflect import get_build, get_default_options
    build = get_build(module)
    default_opts = get_default_options(module)
    opts_json = [] if default_opts is None else [default_opts.jsonify()]

    return json.dumps(build.jsonify() + opts_json)


def main():
    import sys
    assert len(sys.argv) == 2
    project_path = sys.argv[1]
    sys.path.append(project_path)
    import reggaefile
    print(get_json(reggaefile))


if __name__ == '__main__':
    main()
