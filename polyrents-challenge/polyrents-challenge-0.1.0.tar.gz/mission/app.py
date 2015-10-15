# -*- coding: utf-8 -*-
"""
Create the application object containing the two phases

Also add route to listen on /, and redirect to /phase1/
"""

from flask import Flask, redirect, url_for
from . import __name__ as package_name
from .phase1 import phase1
from .phase2 import phase2
import os
import redis


app = Flask(package_name)

app.register_blueprint(phase1)
app.register_blueprint(phase2)


@app.before_first_request
def setup_redis():
    if app.config.get('TESTING'):
        return
    app.redis = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost'))


@app.route('/')
def root():
    return redirect(url_for('phase1.home'), code=301)
