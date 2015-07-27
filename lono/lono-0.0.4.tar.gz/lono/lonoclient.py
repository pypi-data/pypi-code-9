import requests
import json
import re

from device import Device

class LonoClient(object):
    """
    This class is used to communicate with Lono, an internet-of-things
    conencted sprinkler controller and one of the first outdoor smart
    home companies. 
    
    (If you aren't familiar, check us out at http://lono.io)


    A typical workflow for a single user application:
    lc = LonoClient(
        client_id="client id",
        client_secret="client secret",
        redirect_on_success="http://lono.io",
        scope=["write"],
        auth_token="auth token here"
    )
    print "Ready to make requests!"



    A typical workflow for a multi user application:
    lc = LonoClient(
        client_id="client id",
        client_secret="client secret",
        redirect_on_success="http://lono.io",
        scope=["write"]
    )
    # When a user wants to authorize themselves, redirect them:
    print "Redirect a user here:", lc.authorize_url()

    # Once the OAuth2 callback has been called, pass in the auth token
    print "Pass in the auth token on callback:", lc.callback("auth token")

    # and, done!
    print "Ready to make requests!", lc.callback("auth token")
    
    """

    def __init__(self, **kwargs):
        self.opts = kwargs
        self.token = None
        self.api_version = "v1"

        # make sure the user at least specified a device id and secret
        if not self.opts.has_key("client_id") or not self.opts.has_key("client_secret"):
            raise Exception("client_id or client_secret (or both?) wern't specified.")
            

        # api root
        if self.opts.has_key("is_dev") and self.opts["is_dev"]:
            self.site_root = "http://127.0.0.1:3000"
        else:
            self.site_root = "http://make.lono.io"


        # Did user specify auth token? If so, save it.
        if self.opts.has_key("auth_token") and self.opts["auth_token"]:
            self.save_token(self.opts["auth_token"])

    def authorize_url(self, redirect_on_success=None):
        """
        Return the url the user should be redirected to to start the OAuth2
        handshake. 
        
        > lc = LonoClient(client_id="...", ...) # etc...
        > lc.authorize_url()
        """
        return "{0}/dialog/authorize?response_type=code&client_id={1}&redirect_uri={2}&scope={3}".format(
            self.site_root, 
            self.opts["client_id"],
            redirect_on_success or self.opts["redirect_on_success"], 
            ' '.join(self.opts.has_key("scope") and self.opts["scope"] or ["write"])
        )
        
    def save_token(self, token):
        """
        save_token(token)

        Exchange an access token for an auth token. This completes the OAuth2
        handshake. This is synonymous with callback(token).

        > lc = LonoClient(client_id="...", ...) # etc...
        > lc.save_token(token="auth token")
        "access token"
        """
        url = self.site_root + "/oauth/token"

        data = json.dumps({
            "grant_type": "authorization_code",
            "client_id": self.opts["client_id"],
            "client_secret": self.opts["client_secret"],
            "code": token
        })

        headers = {'content-type': 'application/json'}
        r = requests.request("POST", url, data=data, headers=headers)

        if r.status_code == 400:
            raise Exception("Bad client id, secret, or token")
        elif r.status_code == 200:
            body = json.loads(r.text)
            self.token = body["access_token"]
            return {
                "status": "success",
                "data": self.token
            }
        else:
            raise Exception("Unknown error: "+r.text)

    def callback(self, token):
        """
        callback(token)

        Exchange an access token for an auth token. This completes the OAuth2
        handshake. This is synonymous with save_token(token).

        > lc = LonoClient(client_id="...", ...) # etc...
        > lc.callback(token="auth token")
        "access token"
        """
        self.save_token(token)

    def query_device(self, device_id, query):
        """
        query_device(device_id, query)

        Send a query to a lono. This method shouldn't really be used by the
        user (unless you are trying to accomplish something specific) because it
        is called internally to make all of the api calls.

        > lc = LonoClient(client_id="...", ...) # etc...
        > lc.query_device("device id", {"url": "zones/0/on", method: "get"})
        """

        # check both that we have a valid lono id and we have an access token.
        valid_lono_id = re.match("[a-f0-9]{24}", device_id)
        if self.token and valid_lono_id:
            url = "{0}/api/{1}/devices/{2}/{3}".format(
                self.site_root,
                self.api_version,
                device_id,
                query["url"]
            )

            # stringify the body
            data = json.dumps(query.has_key("body") and query["body"] or {})

            headers = {
                "content-type": "application/json",
                "authorization": "bearer {0}".format(self.token)
            }
            r = requests.request(
                query["method"].upper() or "GET",
                url,
                data=data,
                headers=headers,
                timeout=10
            )

            # so, this probably isn't needed here, but we plan on adding some
            # more logic for handling success/error here later TODO
            if r.status_code == 200:
                # success!
                return json.loads(r.text)
            else:
                # error
                return json.loads(r.text)

        elif valid_lono_id:
            raise Exception("No access token has been fetched from the lono cloud")
        else:
            raise Exception("Invalid lono id")

    def get_device(self, device_id):
        return Device(self, device_id)
