from os.path import basename
from subprocess import call
import json

import requests

version = "0.1.3"

class LoginFailed(Exception):
    pass

class Download(dict):
    def __init__(self, game, data, machine_name, platform):
        try:
            # build a nice code name
            self["name"] = machine_name + "-" + data["name"].translate({
                ord(u" "): None,
                ord(u"."): None,
                ord(u"("): None,
                ord(u")"): None
            })
            
            self["game_name"]   = game["name"]
            self["game_title"]  = game["title"]
            self["game_editor"] = game["editor"]
            self["platform"]    = platform
            self["title"]       = data["name"]
            self["human_size"]  = data.get("human_size", "0")
            self["size"]        = data.get("file_size", "0")
            self["sha1"]        = data.get("sha1", None)
            self["md5"]         = data.get("md5", None)
            
            if "url" in data:
                self["url"]     = data["url"].get("web", None)
                self["torrent"] = data["url"].get("bittorrent", None)
            elif "external_link" in data:
                self["url"]     = data["external_link"]
                self["torrent"] = None
            
            if "url" in self and self["url"]:
                self["filename"] = basename(self["url"]).split("?", 1)[0]
            else:
                self["filename"] = None
        
        except KeyError as e:
            print e.args
            print data
            raise

class Game(dict):
    def __init__(self, data):
        self["name"]   = data["machine_name"]
        self["title"]  = data["human_name"]
        self["icon"]   = data["icon"]
        self["url"]    = data["url"]
        self["editor"] = data["payee"]["human_name"]
        
        self.downloads = []
        for download in data["downloads"] :
            platform     = download["platform"]
            machine_name = download["machine_name"]
            for file in download["download_struct"]:
                if "asm_config" in file:
                    continue
                self.downloads.append(Download(self, file, machine_name, platform))

class Order(dict):
    _bundle_url = "https://www.humblebundle.com/downloads?key="
    
    def __init__(self, data):
        self["key"]   = data["gamekey"]
        self["title"] = data["product"]["human_name"]
        self["name"]  = data["product"]["machine_name"]
        self["url"]   = self._bundle_url + self["key"]
        
        self.content = [Game(game) for game in data["subproducts"]]

class Humble(object):
    _url_login        = "https://www.humblebundle.com/login"
    _url_processlogin = "https://www.humblebundle.com/processlogin"
    _url_home         = "https://www.humblebundle.com/home"
    _url_order        = "https://www.humblebundle.com/api/v1/order/"
    
    _gamekeys = []
    
    def __init__(self):
        self._session = requests.Session()
    
    def login(self, email, password):
        login = self._session.get(self._url_login)
        csrf_begin = login.content.find("value='", login.content.find("csrftoken")) + len("value='")
        csrf_end   = login.content.find("'", csrf_begin)
        csrf = login.content[csrf_begin:csrf_end]
        
        payload = {
            "_le_csrf_token": csrf,
            "authy-token"   : "",
            "goto"          : "/home",
            "password"      : password,
            "qs"            : "",
            "submit-data"   : "",
            "username"      : email,
        }
        
        login = self._session.post(self._url_processlogin, data=payload)
        if login.status_code != 200:
            raise LoginFailed(login.status_code)
        if not login.json()["success"]:
            raise LoginFailed(login.status_code)

        self._get_gamekeys()
    
    def _get_gamekeys(self):
        home = self._session.get(self._url_home)
        home = home.content
        fragment = home[home.find("var gamekeys ="):]
        
        fragment = fragment[fragment.find("["):]
        fragment = fragment[:fragment.find("]")+1]
        self._gamekeys += json.loads(fragment)
    
    def keys(self, keys):
        self._gamekeys += keys
    
    def order(self, key):
        url = self._url_order + key
        order = self._session.get(url)
        order = Order(json.loads(order.content))
        
        return order
    
    def orders(self):
        for key in self._gamekeys:
            yield self.order(key)
    
    def games(self):
        games = {}
        
        for order in self.orders():
            for subproduct in order.content:
                games[subproduct["name"]] = subproduct
        
        keys = games.keys()
        keys.sort()
        
        return map(lambda x: games[x], keys)

