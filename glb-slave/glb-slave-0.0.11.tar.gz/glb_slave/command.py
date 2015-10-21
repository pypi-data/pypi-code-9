# -*- coding: utf-8 -*-
import click
from .process import Process


@click.command()
@click.option('-o', '--option',
              type=click.Choice(['start', 'stop', 'restart']), required=True)
@click.option('-h', '--host', required=True, help='the host of the server')
@click.option('-s', '--nginx_switch',
              default=False, is_flag=True,
              help='With nginx service.')
@click.option('-hd', '--haproxy_cfg_dist', required=True,
              default='/etc/haproxy/haproxy.cfg',
              help='native location of haproxy cfg.')
@click.option('-hs', '--haproxy_service_dist', required=True,
              default='/etc/init.d/haproxy',
              help='native location of haproxy service.')
@click.option('-hp', '--haproxy_ssl_dist', required=True,
              default='/etc/haproxy/ssl/',
              help='native location of haproxy ssl pems.')
@click.option('-nc', '--nginx_conf_dist', required=True,
              default='/etc/nginx/nginx.conf',
              help='native location of nginx cfg.')
@click.option('-ns', '--nginx_service_dist', required=True,
              default='service nginx',
              help='native location of haproxy service.')
@click.option('-np', '--nginx_ssl_dist', required=True,
              default='/etc/nginx/ssl/',
              help='native location of nginx ssl pems.')
def process(option, host, nginx_switch,
            haproxy_cfg_dist, haproxy_service_dist, haproxy_ssl_dist,
            nginx_conf_dist, nginx_service_dist, nginx_ssl_dist):
    if option:
        websocket = "ws://%s/websocket" % host
        p = Process(websocket, nginx_switch,
                    haproxy_cfg_dist, haproxy_service_dist, haproxy_ssl_dist,
                    nginx_conf_dist, nginx_service_dist, nginx_ssl_dist)
        if option == 'start':
            print 'glb_slave service start'
            p.start()
        if option == 'stop':
            p.stop()
        if option == 'restart':
            p.restart()
