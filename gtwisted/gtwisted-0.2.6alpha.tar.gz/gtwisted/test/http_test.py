#coding:utf8
'''
Created on 2015-7-7

@author: root
'''
import gevent.monkey
from flask.templating import render_template
from werkzeug import redirect
gevent.monkey.patch_all()

from flask import Flask
from gtwisted.core import reactor
import memcache

app = Flask(__name__)
app.debug = True
mc = memcache.Client(["127.0.0.1:11211"])
mc.set("a",1)

@app.route('/')
def choose_name():
    
    return 1#str(mc.get("a"))



reactor.listenWSGI(8080, app)
reactor.run()