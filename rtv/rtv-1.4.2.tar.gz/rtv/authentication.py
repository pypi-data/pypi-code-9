# Rate limiting:
#     Unauthenticated clients may make up to 30 requests per minute [1]
#     Oauth2 clients may make up to 60 requests per minute [1]
#     For application-only authentication for a single server, rate limiting
#     is per app. For a mobile app, they're looser and track per-ip. For
#     logged-in usage it's per user [4].
#     For unauthenticated client-only, use client_credentials.


# (1) https://github.com/reddit/reddit/wiki/API
# (2) https://github.com/reddit/reddit/wiki/OAuth2
# (3) http://praw.readthedocs.org/en/latest/pages/oauth.html
# (4) https://www.reddit.com/r/redditdev/comments/336p8k
# (5) https://www.reddit.com/r/redditdev/comments/2ujhkr

# As of July 19, 2015, Reddit supports 3 oAuth workflows: Installed app,
# Web app, and Script app. Of the 3, Installed app is the only route that does
# not require an API secret key. Because this is an open source project, using
# a secret key would require EVERYONE who uses this app to go to
# https://www.reddit.com/prefs/apps and register for a new application. I
# believe that this is an extremely annoying hoop to jump through and goes
# against the intentions of oAuth. As of PRAW v3.1.0 there is no implementation
# for the Installed app workflow.

CLIENT_ID = '_Yw4NOl8UD9z9g'
REDIRECT_URI = 'http://127.0.0.1:65013'
SCOPE = ['edit', 'history', 'identity', 'privatemessages', 'read', 'submit', 'vote']

# https://github.com/reddit/reddit/wiki/OAuth2#authorization-implicit-grant-flow
#
# Authorization URL:
#     https://www.reddit.com/api/v1/authorize
# Payload:
#     client_id     = CLIENT_ID
#     response_type = the string "token"
#     state         = a unique random string
#     redirect_uri  = REDIRECT_URI
#     scope         = edit,history,identity,privatemessages,read,submit,vote

import requests
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlparse
import praw

LOGIN_URI = 'https://www.reddit.com/api/login'
USERNAME = 'civilization_phaze_3'
PASSWORD = 'VGNfw29)'

reddit = praw.Reddit('hello world')
reddit.client_id = CLIENT_ID
reddit.redirect_uri = REDIRECT_URI
#
# # potentially switch to reddit.request()
# session = requests.session()
# session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36'
#
#
#
#
#     def request(self, url, params=None, data=None, retry_on_error=True,
#                 method=None):
#
#
# print('a')
# data = {
#     'op': 'login',
#     'user': USERNAME,
#     'passwd': PASSWORD,
#     'api_type': 'json'}
# response = session.post(LOGIN_URI,
#                         data=data)
# print('b')
# payload = {
#     'client_id': CLIENT_ID,
#     'response_type': 'token',
#     'state': 'hello',
#     'redirect_uri': REDIRECT_URI,
#     'scope': ','.join(SCOPE)}
#
# response = session.get(reddit.config['authorize'], params=payload)
# soup = BeautifulSoup(response.content, 'html.parser')
# form = soup.find('form', action='/api/v1/authorize')
# payload = {f['name']: f['value'] for f in form.find_all(name='input') if f['value'] != 'Decline'}
# response = session.post('https://www.reddit.com/api/v1/authorize', data=payload, allow_redirects=False)
# assert response.status_code == 302
# pass

# Need to handle 503 - servers are busy

# Obtaining an auth token is a 3-step process:
# 1. Login to