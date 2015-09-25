from hammock import Hammock
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)




# https://docs.saltstack.com/en/latest/topics/netapi/index.html
#from salt.netapi import NetapiClient


class RestClient():
    def __init__(self, opts):
        self.master = opts['master']
        self.port = opts.get('port', 80)
        self.username = opts['username']
        self.password = opts['password']
        self.eauth = opts.get('eauth', 'pam')
        self.session = Hammock("http://%(master)s:%(port)s" % opts)
        self._auth = dict(
            username=self.username,
            password=self.password,
            eauth=self.eauth,
        )

    def login(self):
        resp = self.session.login.POST(data=self._auth)
        assert resp.status_code == 200, resp.text

    def logout(self):
        resp = self.session.logout.POST()
        assert resp.status_code == 200, resp.text

    def run(self, tgt=None, fun=None, arg=None,
            client='local', expr_form='glob',
            **kwargs):
        data = dict(
            tgt=tgt, fun=fun, client=client, arg=arg,
            expr_form=expr_form,
            )
        log.debug("run: %s", data)
        #data = {k:v for k,v in data.items() if v}
        data.update(self._auth)
        resp = self.session.run.POST(data=data)
        assert resp.status_code == 200, resp.text
        return resp.json()

    def minions_run(self, tgt=None, fun=None, arg=None,
                    client='local', expr_form='glob',
                    **kwargs):
        data = dict(
            tgt=tgt, fun=fun, client=client, arg=arg,
            expr_form=expr_form,
            )
        data.update(self._auth)
        resp = self.session.minions.POST(data=data)
        assert resp.status_code == 202, resp.text
        return resp.json()

    def minions(self):
        resp = self.session.minions.GET()
        assert resp.status_code == 200, resp.text
        return resp.json()

    def jobs(self, jid=None):
        data = dict(jid=jid)
        data.update(self._auth)
        if jid:
            resp = self.session.jobs.GET(jid)
        else:
            resp = self.session.jobs.GET()
        assert resp.status_code == 200, resp.text
        return resp.json()
