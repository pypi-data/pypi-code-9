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
import time

import Adafruit_BBIO.UART as UART
import flask
from gsmmodem.modem import GsmModem
from gsmmodem.modem import CmsError


PORT = 'UART1'
DEVICE = '/dev/ttyO1'
BAUD = 9600


# Setup the logger, a serial port, and the flask app.
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
UART.setup(PORT)
app = flask.Flask(__name__)


def handle_incoming_call(incoming_call):
  """Callback that will run when a call comes in."""
  if incoming_call.ringCount >= 2:
    incoming_call.answer()
    time.sleep(5)
    if incoming_call.answered:
      incoming_call.hangup()


@app.before_first_request
def setup_modem():
  """Setup the GSM Modem."""
  flask.g.modem = GsmModem(
    DEVICE, BAUD, incomingCallCallbackFunc=handle_incoming_call)
  flask.g.modem.connect()


@app.route('/')
def index():
  """Get Node info."""
  return flask.jsonify(
    imsi=flask.g.modem.imsi,
    model=flask.g.modem.model,
    manufacturer=flask.g.modem.manufacturer,
    network_name=flask.g.modem.networkName,
    signal_strength=flask.g.modem.signalStrength,
  )


@app.route('/sms', methods=['POST'])
def sms():
  """Send an SMS.

  Expected POST data: phone_number, message
  """
  phone_number = flask.request.form['phone_number']
  message = flask.request.form['message']
  try:
    flask.g.modem.sendSms(phone_number, message)
    return ''
  except CmsError as error:
    # CMS error 2172 is raised if there is no network coverage.
    return 'error: %s' % str(error), 503


@app.route('/call', methods=['POST'])
def call():
  """Initiate a call.

  Expected POST data:
    phone_number: a number to dial
    hangup_after: after the call is answered, hangup after this many seconds
  """
  phone_number = flask.request.form['phone_number']
  hangup_after = int(flask.request.form['hangup_after'])
  current_call = flask.g.modem.dial(phone_number)
  start_time = time.time()
  while current_call.active:
    if current_call.answered:
      if start_time + hangup_after > time.time():
        current_call.hangup()
    time.sleep(1)


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
  # View the SMS log.
  if flask.request.method == 'GET' and activity == 'sms':
    messages = []
    for message in flask.g.modem.listStoredSms():
      messages.append({
        'time': message.time,
        'number': message.number,
        'text': message.text,
      })
    return flask.jsonify(
      messages=messages,
    )
  # Clear the SMS log.
  # Note(matt): the gsmmodem docs suggest using listStoredSms(delete=True)
  # to clear the sms log but I've had issues with the AT+CMGD used by that
  # method (you have to specify a valid index, not just 1).  I've found that
  # processStoredSms does the trick though.
  elif flask.request.method == 'DELETE' and activity == 'sms':
    flask.g.modem.processStoredSms()
    return ''
