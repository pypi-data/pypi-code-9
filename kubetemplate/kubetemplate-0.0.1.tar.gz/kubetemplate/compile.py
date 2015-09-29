import os
import shutil
import glob

from kubetemplate import utils, helpers

__j = None # Jinja compiler

''' command line compile wrapper. parses command line arguments and .kubetemplate file '''
# def compile(input_t=None, output_t=None):
def compile(
        input_t : 'input target path, defaults to targets in .kubetemplate file' = None,
        output_t : 'output target path if input target path specified, defaults to same directory' = None,
        ):
    if input_t is not None:
        return compile_t(input_t, output_t)
    else: # default to .kubetemplate file
        for t in utils.props()['compiler']['targets']:
            to = t.get('to')
            to = to and utils.root_path(to)
            path = utils.root_path(t['path'])
            compile_t(path, to)

'''
    compile a glob-able path input_t
    output directory ouput_t when input_t is a file or directory, undefined behaviour for glob-able input_t
'''
def compile_t(
        input_t : 'input target path',
        output_t : 'output target path, defaults to same path' = None,
        ):

    input_t = os.path.abspath(input_t)
    output_t = output_t and os.path.abspath(output_t)

    for g in glob.glob(input_t):
        if os.path.isdir(g):
            for f in [
                    os.path.join(di, fi)
                    for (di, _, fis) in os.walk(g)
                    for fi in fis
                ]:
                outd = output_t \
                    and os.path.join(
                        output_t,
                        os.path.relpath(f, g)
                    ) \
                    or f
                outd = os.path.dirname(outd)
                compile_file(f, outd)
        else:
            outd = output_t or os.path.dirname(input_t)
            compile_file(g, outd)

''' compiles a single file '''
def compile_file(input_f, output_d):

    global __j
    if __j is None:
        context = utils.props()

        context['helpers'] = helpers.helpers

        __j = JinjaCompiler('/', context)

    path, file_name = os.path.split(input_f)
    fname, ext = os.path.splitext(file_name)

    output_prefix = __j.env.globals['config'].get('compiler', {}).get('output_prefix', '')

    if ext == '.jinja':
        os.makedirs(output_d, exist_ok=True)
        output_f = os.path.join(output_d, '{}{}'.format(output_prefix, fname))

        print(input_f)

        __j.compile(input_f, output_f)

        return output_f

class JinjaCompiler:
    def __init__(self, root_dir, config):
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(root_dir))
        self.env.globals['config'] = config

    def compile(self, in_file, out_file, config={}):
        with open(out_file, 'w') as f:
            f.write(self.env.get_template(in_file).render(config))
