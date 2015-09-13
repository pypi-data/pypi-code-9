#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response

from flask.ext.iniconfig import INIConfig

app = Flask(__name__)
INIConfig(app)
app.config.from_inifile('test.ini')

@app.route('/')
def index():
    def generate():
        for key, value in app.config.items():
            yield '%s: %s\n' % (key, value)
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
