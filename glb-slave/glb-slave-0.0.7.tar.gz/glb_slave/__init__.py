# -*- coding: utf-8 -*-
import click
from process import Process


@click.command()
@click.argument('option', required=True)
@click.option('-h', '--host', required=True, help='the host of the server')
@click.option('-d', '--dist', required=True,
              default='/etc/haproxy/haproxy.cfg',
              help='native location of haproxy cfg.')
@click.option('-s', '--s_dist', required=True,
              default='/etc/init.d/haproxy',
              help='native location of haproxy service.')
@click.option('-p', '--p_dist', required=True,
              default='/etc/haproxy/ssl/',
              help='native location of ssl pems.')
def process(option, host, dist, s_dist, p_dist):
    if option:
        websocket = "ws://%s/websocket" % host
        p = Process(websocket, dist, s_dist, p_dist)
        if option == 'start':
            p.start()
        if option == 'stop':
            p.stop()
        if option == 'restart':
            p.restart()
