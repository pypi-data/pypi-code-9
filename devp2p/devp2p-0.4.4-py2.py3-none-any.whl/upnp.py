from urllib import urlopen
import miniupnpc
from slogging import get_logger
log = get_logger('upnp')


def get_public_ip():
    return urlopen('http://icanhazip.com/').read().strip()


def upnp_add(port):
    '''
    :param port: local port
    :return: `dict(`external_ip`=str, `external_port`=int) if succeed or empty dict
    '''
    log.debug('Setting UPNP')

    upnpc = miniupnpc.UPnP()
    upnpc.discoverdelay = 200
    ndevices = upnpc.discover()
    log.debug('UPNP device(s) detected', num=ndevices)

    if not ndevices:
        return dict()

    upnpc.selectigd()
    try:
        external_ip = upnpc.externalipaddress()
    except Exception:
        log.warn('could not lookup external ip')
        return dict()

    log.debug('upnp results', external_ip=external_ip,
              status=upnpc.statusinfo(),
              connection_type=upnpc.connectiontype())

    # find a free port for the redirection
    external_port = port
    found = False

    while True:
        redirect = upnpc.getspecificportmapping(external_port, 'TCP')
        if redirect is None:
            found = True
            break
        if external_port >= 65535:
            break
        external_port += 1

    if not found:
        log.debug('No redirect candidate', external_ip=external_ip,
                  lan_ip=upnpc.lanaddr, lan_port=port)
        return dict()

    log.debug('trying to redirect', external_ip=external_ip, external_port=external_port,
              lan_ip=upnpc.lanaddr, lan_port=port)

    res = upnpc.addportmapping(external_port, 'TCP',
                               upnpc.lanaddr, port,
                               'devp2p port %u' % external_port,
                               '')

    if res:
        log.debug('success to redirect', external_ip=external_ip, external_port=external_port,
                  lan_ip=upnpc.lanaddr, lan_port=port)
    else:
        return dict()
    return dict(external_ip=external_ip, external_port=external_port)


def upnp_delete(upnpc, external_port):
    res = upnpc.deleteportmapping(external_port, 'TCP')
    if res:
        log.debug('successfully deleted port mapping')
        return True
    log.debug('failed to remove port mapping')
    return False
