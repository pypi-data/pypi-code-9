import click
import importlib

def parse_modules_list(modules):
    return [parse_module(m) for m in modules]

def parse_module(module):
    """
    Supported formats:
        * plain string
        * {module: display_name}
        * {name: name, module: module, cli: cli}
            `name` or `module` are mandatory
    """
    if isinstance(module, str):
        return {'name': module, 'module': module}
    if isinstance(module, dict):
        if 'name' in module and 'module' in module:
            return module
        if 'name' in module and 'module' not in module:
            module['module'] = module['name']
            return module
        if 'module' in module and 'name' not in module:
            module['name'] = module['module']
            return module
        if len(module) == 1:
            return {'name': module.values()[0], 'module': module.keys()[0]}
    raise TypeError('Unknown module definition format')


class DynoCli(click.MultiCommand):

    def __init__(self, modules, *args, **kwargs):
        self.modules = parse_modules_list(modules)
        super(DynoCli, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        return sorted(m['name'] for m in self.modules)

    def get_command(self, ctx, name):
        if name not in self.list_commands(ctx):
            return ctx.fail('No such command "%s"' % name)
        module_def = [m for m in self.modules if m['name'] == name][0]
        try:
            module = importlib.import_module("{module}.cli".format(module=module_def['module']))
        except ImportError:
            raise ImportError("Could not find CLI module for %s" % name)
        if not hasattr(module, 'cli'):
            raise ImportError("{module}.cli does not have `cli` object".format(module_def['module']))
        if module_def.get('cli'):
            ctx.obj = module_def.get('cli')
        return module.cli

