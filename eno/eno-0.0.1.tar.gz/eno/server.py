"""Control server.

This server runs on each eno node, exposing various endpoints so data can be
sent to the node and so we can read data back:

  * GET / to show node info
  * POST /sms to send a message
  * POST /call to initiate a call
  * POST /hangup to hangup an in-progress call
  * POST /data to access a webpage
  * GET /log/<activity> shows logs for calls, SMS and data usage
  * DELETE /log/<activity> to clear usage logs
"""

import flask


app = flask.Flask(__name__)


@app.route('/')
def index():
  """Get Node info."""


@app.route('/sms', methods=['POST'])
def sms():
  """Send an SMS."""


@app.route('/call', methods=['POST'])
def call():
  """Initiate a call."""


@app.route('/hangup', methods=['POST'])
def hangup():
  """Hangup any in-progress calls."""


@app.route('/data', methods=['POST'])
def data():
  """Access a webpage."""


@app.route('/log/<activity>', methods=['GET', 'DELETE'])
def log(activity):
  """Call, SMS and data usage history.

  GET to view the data or DELETE to erase it.
  """
