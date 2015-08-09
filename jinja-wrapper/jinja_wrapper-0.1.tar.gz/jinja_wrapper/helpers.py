from os import listdir
from os.path import isdir, join
from jinja2 import Environment, FileSystemLoader

def find_template(search_path, target):
    for path in search_path:
        for f in listdir(path):
            if (isdir(join(path, f)) and (f == target)):
                    return join(path, f)
    return None

def write_file_template(template_name, values, target, opts):
    """
    Write template based on FileSystemLoader
    Args:
        template_name String
        values Dict: values for template
        target IO: io object with 'write' method
        opts Hash
            search_path String|List
    """
    search_path = opts.pop('search_path')
    env = Environment(loader=FileSystemLoader(search_path), **opts)
    template = env.get_template(template_name)
    output = template.render(values)

    if target == 'stdout':
        import sys
        target = sys.stdout
    return target.write(output)

