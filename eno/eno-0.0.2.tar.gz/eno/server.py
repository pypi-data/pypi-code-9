"""Control server.

This server runs on the Beaglebone Black of each eno node, exposing various
endpoints so data can be sent to the node and so we can read data back:

  * GET / to show node info
  * POST /sms to send a message
  * POST /call to initiate a call
  * POST /hangup to hangup an in-progress call
  * POST /data to access a webpage
  * GET /log/<activity> shows logs for calls, SMS and data usage
  * DELETE /log/<activity> to clear usage logs
"""

import logging

import Adafruit_BBIO.UART as UART
import flask
from gsmmodem.modem import GsmModem


PORT = 'UART1'
DEVICE = '/dev/ttyO1'
BAUD = 9600


# Setup the logger, a serial port, and the flask app.
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
UART.setup(PORT)
app = flask.Flask(__name__)


@app.route('/')
def index():
  """Get Node info."""
  modem = GsmModem(DEVICE, BAUD)
  modem.connect()
  try:
    return flask.jsonify(
      imsi=modem.imsi,
      model=modem.model,
      manufacturer=modem.manufacturer,
      network_name=modem.networkName,
      signal_strength=modem.signalStrength,
    )
  finally:
    modem.close()


@app.route('/sms', methods=['POST'])
def sms():
  """Send an SMS.

  Expected POST data: phone_number, message
  """
  phone_number = flask.request.form['phone_number']
  message = flask.request.form['message']
  modem = GsmModem(DEVICE, BAUD)
  modem.connect()
  modem.sendSms(phone_number, message)
  modem.close()
  return ''


@app.route('/call', methods=['POST'])
def call():
  """Initiate a call.

  Expected POST data: phone_number, hangup_immediately
  """


@app.route('/hangup', methods=['POST'])
def hangup():
  """Hangup any in-progress calls.

  Expected POST data: (none)
  """


@app.route('/data', methods=['POST'])
def data():
  """Access a webpage."""


@app.route('/log/<activity>', methods=['GET', 'DELETE'])
def log(activity):
  """Call, SMS and data usage history.

  GET to view the data or DELETE to erase it.
  """
  # Validate.
  if activity not in ('sms', 'call', 'data'):
    return '', 400
  # Setup the GSM modem.
  modem = GsmModem(DEVICE, BAUD)
  modem.connect()
  # View the SMS log.
  if flask.request.method == 'GET' and activity == 'sms':
    messages = []
    for message in modem.listStoredSms():
      messages.append({
        'time': message.time,
        'number': message.number,
        'text': message.text,
      })
    modem.close()
    return flask.jsonify(
      messages=messages,
    )
  # Clear the SMS log.
  elif flask.request.method == 'DELETE' and activity == 'sms':
    modem.listStoredSms(delete=True)
    return ''
