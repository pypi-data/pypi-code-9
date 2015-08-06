"""Local test server for cmcic payment system.

Start it with:

./localtestserver.py [accept|reject] path/to/tpe.cfg

First argument is action in response to payment request: accept or reject.
Second argument is full path to tpe config file.
"""

import sys, cgi, BaseHTTPServer, urlparse, urllib, urllib2

index_html = '''<h1>Local test server for CM-CIC paiement</h1>
<p>%sing payment requests for TPE %s (%s)</p>
'''

pay_html = '''<p>Received payment request:</p>
%s
<p>Sending response:</p>
%s
<p>Response sent to %s and and got return value %s.</p>
<p>Return to the site at <a href="%s">%s</a>.</p>
'''

def dict_as_html_table(map):
    html = '<table>'
    for key in sorted(map):
        html += '<tr><td>%s</td><td>%s</td></tr>' % (repr(key), repr(map[key]))
    html += '</table>'
    return html

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def _read_form(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        length = int(self.headers.getheader('content-length'))
        if ctype == 'multipart/form-data':
            self.form = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            query = self.rfile.read(length)
            self.form = cgi.parse_qs(query, keep_blank_values=1)
        else:
            self.form = {}

    def do_GET(self):
        if self.path == '/':
            body = index_html % (self.server.action,
                                 self.server.tpe.tpe_company,
                                 self.server.tpe.tpe_number)
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404,'Not found')

    def do_POST(self):
        self._read_form()
        if self.path.startswith('/paiement.cgi'):
            req = self.read_paymentrequest()
            rep = self.build_paymentresponse(req)
            ack = self.send_paymentresponse(rep)
            body = index_html % (self.server.action,
                                 self.server.tpe.tpe_company,
                                 self.server.tpe.tpe_number)
            if self.server.action == 'accept':
                next_url = req.url_ok
            else:
                next_url = req.url_err
            body += pay_html % (dict_as_html_table(req.as_dict()),
                                dict_as_html_table(rep.as_dict()),
                                self.server.tpe.return_url,
                                ack, next_url, next_url)
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404, 'Not found')

    def read_paymentrequest(self):
        params = dict([(key,value[0]) for key,value in self.form.items()])
        return self.server.tpe.read_paymentrequest(params)

    def build_paymentresponse(self, req):
        rep = cmcic.PaymentResponse()
        for attr in 'reference amount date description'.split():
            setattr(rep, attr, getattr(req, attr))
        if self.server.action == 'accept':
            rep.return_code = 'payetest'
        elif self.server.action == 'reject':
            rep.return_code = 'Annulation'
        msg, mac = self.server.tpe.paymentresponse_msg(rep)
        rep.mac = mac
        return rep

    def send_paymentresponse(self, rep):
        try:
            ack = urllib2.urlopen(self.server.tpe.return_url, urllib.urlencode(rep.as_dict())).read()
        except urllib2.HTTPError, exc:
            ack = str(exc)
        return ack

if __name__ == '__main__':
    import cmcic
    action = sys.argv[1]
    cfg = sys.argv[2]
    tpe = cmcic.get_tpe(cfg)
    port = int(urlparse.urlparse(tpe.server_url)[1].split(':')[1])
    httpd = BaseHTTPServer.HTTPServer(('', port), RequestHandler)
    httpd.tpe = tpe
    httpd.action = action
    httpd.serve_forever()

