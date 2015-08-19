'''
Created on May 29, 2015

@author: martin.melchior
'''
import optparse

from euclid_wfm.euclidwf.server import server_views_flask


STATIC_FILES='STATIC_FILES'

def start_server(args):
    port=args.port
    cfgfile=args.config
    print 'Twisted on port {port}...'.format(port=port)
    from twisted.internet import reactor
    from twisted.web.server import Site
    from twisted.web.wsgi import WSGIResource

    app = server_views_flask.app
    configure(app, cfgfile)
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)
    reactor.listenTCP(port, site, interface="0.0.0.0")
    reactor.run()


def configure(app, cfgfile):
    app.config.from_pyfile(cfgfile)
    app.static_folder=app.config[STATIC_FILES]
    

def parse_args():
    parser = optparse.OptionParser(usage="%prog [options]  or type %prog -h (--help)")
    #parser.add_option('--port', help='Twisted event-driven web server', action="callback", callback=start_server, type="int");
    parser.add_option('-p', '--port', dest='port', default=701, help='Port to run the server at.', type="int")
    parser.add_option('-c', '--config', dest='config', help='Config file for setting up the server.')
    return parser.parse_args()


def main():
    args,_=parse_args()
    start_server(args)

if __name__ == "__main__":
    main()
