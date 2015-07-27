""" Sessions represent specific browser emulation attempts to prime specific
caches. It's a collection of an instance of the fake browser with the associated
settings required to hit a site.
"""

from robobrowser import RoboBrowser
from urllib.parse import urlsplit

class Session(object):

    def __repr__(self):
        if self.cookie is None:
            return "<Primer Session @ {}>".format(self.url)
        else:
            return "<Primer Session @ {} (via {})>".format(self.url, self.cookie)

    def __init__(self, url, username, password, cookie=None):
        self.url = url
        self.domain = urlsplit(self.url).netloc
        self.username = username
        self.password = password
        self.cookie = cookie
        self.state = "Unprimed"

        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36"
        self.browser = RoboBrowser(parser="html.parser", user_agent=user_agent)
        if self.cookie is not None:
            for key,val in self.cookie.items():
                self.browser.session.cookies.set(key, val, domain=self.domain)

    def prime_cache(self):
        self.browser.open(self.url)
        form = self.browser.get_form(id="loginForm")
        form['UserName'].value = self.username
        form['Password'].value = self.password
        self.browser.submit_form(form)
        self.browser.submit_form(self.browser.get_form())

        # probably should test outcome, huh. 
        if urlsplit(self.browser.response.url).netloc == self.domain:
            self.state = "Primed"
        else:
            self.state = "Errored"