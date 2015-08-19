import json


class ReggaeEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'jsonify'):
            return o.jsonify()
        else:
            super().default(o)


def get_json(module):
    from reggae.reflect import get_build
    return json.dumps(get_build(module), cls=ReggaeEncoder)


def main():
    import sys
    assert len(sys.argv) == 2
    project_path = sys.argv[1]
    sys.path.append(project_path)
    import reggaefile
    print(get_json(reggaefile))


if __name__ == '__main__':
    main()
