from flask import Flask

from stuffproxy.config import settings

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! %s" % settings.project.hostname
