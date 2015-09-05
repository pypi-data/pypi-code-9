#!/usr/bin/python2
__author__ = "frank"

# ==============================================================================
#      Frank Matranga's Third-party Regis High School Python Module
# ==============================================================================

import sys
import os
from scraper import Scraper
from cli import CLI
from viewer import Viewer
import json
from pymongo import MongoClient
import requests
from lxml import html

VERSION = "0.1"
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/secrets.json"
DB_NAME = "regis"
IP = "localhost"
PORT = "27017"

class TRP:
    def __init__(self, path=PATH):
        self.path = path
        print " --- Initalizing TRP Module v"+VERSION+" ---\n"
        #print "Arguments: "+str(sys.argv[1::])
        self.secrets = self.get_secrets()
        self.username = self.secrets['regis_username']
        self.password = self.secrets['regis_password']
        print "Found info for Regis student '"+self.username+"'"
        self.connect_to_db()
        self.session = self.get_session()
        self.init_mods()
        print "\n --- READY --- \n"
    def get_secrets(self):
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            self.path = sys.argv[1]

        try:
            secrets = json.loads(open(self.path).read())
        except (ValueError, IOError):
            print "No valid secrets.json found"
            self.exit()

        print "Using path '"+self.path+"' for secrets.json"
        return secrets

    def connect_to_db(self):
        try:
            print "Attempting to connect to mongodb://"+IP+":"+PORT+"/"+DB_NAME+"..."
            self.client = MongoClient('mongodb://'+IP+':'+PORT+'/')
            self.db = self.client[DB_NAME]
            self.db.students.count()
            print "Done..."
        except Exception: # nasty I know
            self.client = None
            print "Failed to connect to Database."
            self.exit()
    def get_session(self):
        print "Attempting logins..."
        url = "https://moodle.regis.org/login/index.php"
        values = {'username': self.username, 'password': self.password}
        session = requests.Session()
        r = session.post(url, data=values)
        parsed_body = html.fromstring(r.text)
        title = parsed_body.xpath('//title/text()')[0]

        # Check whether login was successful or not
        if not "My home" in title:
            print "Failed to login to Moodle, check your credentials."
            self.exit()
        print "Logged into Moodle."

        url = "https://intranet.regis.org/login/submit.cfm"
        values = {'username': self.username, 'password': self.password, 'loginsubmit': ''}
        r = session.post(url, data=values)
        parsed_body = html.fromstring(r.text)
        try:
            title = parsed_body.xpath('//title/text()')[0]
            if not "Intranet" in title:
                print "Failed to login to the Intranet, check your credentials."
                quit()
        except:
            print "Failed to login to the Intranet, check your credentials."
            quit()

        print "Logged in to the Intranet."
        print "Done..."
        return session

    def init_mods(self):
        print "Initialzing modules..."
        self.viewer = Viewer(self.db)
        self.scraper = Scraper(self.db, self.session)
        self.cli = CLI(self.db)
        print "Done..."

    def exit(self):
        try: # this might be run before it is assigned
            self.client.close()
            print "Closed DB connection."
        except:
            pass

        print "Shutting down..."
        quit()
        sys.exit()

def main():
    t = TRP()
    t.cli.run()

if __name__ == "__main__":
    main()
