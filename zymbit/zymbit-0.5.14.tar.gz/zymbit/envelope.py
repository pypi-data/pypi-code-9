import json
import uuid

from zymbit.timeutil import timestamp

# different ways a data stream buffer is parsed in order to ship up
# NOTE: first one to send back an envelope wins, so order matters!
ENVELOPE_PARSERS = []


def parse_json_envelope(buf):
    action = 'data'

    try:
        params = json.loads(buf)
    except ValueError:
        return None
    else:
        if isinstance(params, int):
            params = {
                'key': 'sensor',
                'value': params,
            }

        return get_envelope(action, params)
ENVELOPE_PARSERS.append(parse_json_envelope)


def parse_comma_equals(buf):
    """
    Parse a string of comma-delimited strings, that are each equal-delimited key/value pairs
    :param buf: string - buffer to be parsed
    :return: None - when no equal sign is found, JSON string envelop - when data is parsed
    """
    if '=' not in buf:
        return None

    parsed = {}
    unparsed = []

    # split at commas
    for token in buf.split(','):
        # get rid of outer spaces
        token = token.strip()

        if '=' not in token:
            unparsed.append(token)
            continue

        key, value = token.split('=')
        key = key.strip()

        if ' ' in key:
            _unparsed, key = key.rsplit(' ', 1)
            unparsed.append(_unparsed)

        for conversion in (int, float):
            try:
                value = conversion(value)
            except ValueError:
                pass
            else:
                break

        parsed[key] = value

    if unparsed:
        parsed['zb.unparsed'] = json.dumps(unparsed)
        parsed['zb.unparsed.line'] = buf

    return get_envelope('data', parsed)


ENVELOPE_PARSERS.append(parse_comma_equals)


# NOTE: this is the "if all else fails" parser; should be appended last!
def parse_log_envelope(buf):
    return get_envelope('log', {
        'line': buf,
    })
ENVELOPE_PARSERS.append(parse_log_envelope)


def get_envelope(action, params, client_id=None, as_json=True):
    data = {
        'message_id': str(uuid.uuid4()),
        'timestamp': timestamp(),
        'action': action,
        'params': params,
    }

    if client_id:
        data.update({
            'client_id': client_id,
        })

    if as_json:
        return json.dumps(data)
    else:
        return data


def parse_buf(buf):
    """
    parse the given buffer into an envelope
    :param buf: string, may be in a parseable format
    :return: envelope
    """
    for parser in ENVELOPE_PARSERS:
        envelope = parser(buf)
        if envelope:
            return envelope
