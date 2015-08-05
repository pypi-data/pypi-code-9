import time
import click

import xpcs.globals
import xpcs.exc


def make_filterfunc(filter):
    filtermap = {
        'offline': 'online',
        'clean': 'unclean',
        'in-use': 'standby',
        'running': 'shutdown'}

    if filter == 'all':
        filterfunc = lambda node: True
    elif filter in ['online', 'standby', 'shutdown', 'unclean',
                    'maintenace']:
        filterfunc = lambda node: node[filter] == 'true'
    elif filter in filtermap:
        filter = filtermap[filter]
        filterfunc = lambda node: node[filter] == 'false'
    else:
        raise ValueError(filter)

    return filterfunc


@click.group('node')
def cli():
    pass


@cli.command('is-online')
@click.argument('name')
@click.pass_context
def is_managed(ctx, name):
    '''Check if the given node is online'''
    state = ctx.obj.node(name)['online'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s online' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-standby')
@click.argument('name')
@click.pass_context
def is_standby(ctx, name):
    '''Check if the given node is standby'''
    state = ctx.obj.node(name)['standby'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s standby' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('is-shutdown')
@click.argument('name')
@click.pass_context
def is_shutdown(ctx, name):
    '''Check if the given node is shutdown'''
    state = ctx.obj.node(name)['shutdown'] == 'true'
    if not xpcs.globals.quiet:
        print 'node %s %s shutdown' % (
            name,
            'is' if state else 'is not')
    ctx.exit(int(not state))


@cli.command('wait')
@click.option('--timeout', '-t', default=0)
@click.option('--online', 'filter', flag_value='online', default=True)
@click.option('--offline', 'filter', flag_value='offline')
@click.option('--standby', 'filter', flag_value='standby')
@click.option('--in-use', 'filter', flag_value='in-use')
@click.option('--shutdown', 'filter', flag_value='shutdown')
@click.option('--unclean', 'filter', flag_value='unclean')
@click.option('--clean', 'filter', flag_value='clean')
@click.option('--maintenance', 'filter', flag_value='maintenance')
@click.argument('nodes', nargs=-1, default=None)
@click.pass_context
def wait(ctx, timeout=0, filter=None, nodes=None):
    '''Wait for a node to reach a given state'''
    filterfunc = make_filterfunc(filter)
    wait_start = time.time()

    while True:
        if not len(nodes):
            _nodes = [node for node in ctx.obj.nodes]
        else:
            _nodes = [node for node in ctx.obj.nodes
                      if node['name'] in nodes]

        matched = any(not filterfunc(node) for node in _nodes)

        if not matched:
            break

        if timeout and (time.time() >= wait_start + timeout):
            raise xpcs.exc.TimeoutError(
                'Timed out while waiting for nodes')

        time.sleep(1)


@cli.command('list')
@click.option('--all', 'filter', flag_value='all', default=True)
@click.option('--online', 'filter', flag_value='online')
@click.option('--offline', 'filter', flag_value='offline')
@click.option('--standby', 'filter', flag_value='standby')
@click.option('--in-use', 'filter', flag_value='in-use')
@click.option('--shutdown', 'filter', flag_value='shutdown')
@click.option('--unclean', 'filter', flag_value='unclean')
@click.option('--clean', 'filter', flag_value='clean')
@click.option('--maintenance', 'filter', flag_value='maintenance')
@click.pass_context
def list(ctx, filter='all'):
    '''List nodes'''
    filterfunc = make_filterfunc(filter)
    print '\n'.join(node['name'] for node in ctx.obj.nodes
                    if filterfunc(node))
