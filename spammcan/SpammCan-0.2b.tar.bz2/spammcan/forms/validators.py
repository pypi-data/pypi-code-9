"""Basic custom validators."""

__all__ = [
    'Range',
    'SpamBayesFilter',
    'ValidFormat',
    'ValidModelValue',
    'ValidPasteGuid',
    'ValidStyle',
]

import logging
import socket
import xmlrpclib

from sqlalchemy.exceptions import InvalidRequestError
from turbogears import config, validators
from turbojson.jsonify import jsonify

from spammcan import model


log = logging.getLogger('spammcan.controllers')


class ValidModelValue(validators.FancyValidator):
    """Check if given value is a valid key to an existing model object.
    """

    class_ = None
    attr = 'id'
    name = 'value'
    convert_value = True

    messages = {
        'notExistant': u"There is no %(class_)s with the %(name)s '%(value)s'."
    }

    def _to_python(self, value, state):
        model_cls = getattr(model, self.class_ or '', None)
        try:
            if model_cls:
                model_inst = model_cls.query.filter_by(
                    **{self.attr: value}).one()
            else:
                msg = u'Model class %s not found.' % self.class_
                log.debug(msg)
                raise ValueError(msg)
        except (ValueError, InvalidRequestError), exc:
            log.debug('Could not validate %s.%s == %r: %r',
                    self.class_, self.class_, value, exc)
            raise validators.Invalid(self.message('notExistant', state,
                class_=self.class_, name=self.name, value=value), value, state)
        if self.convert_value:
            return model_inst
        else:
            return value

class ValidPasteGuid(ValidModelValue):
    class_ = 'Paste'
    attr = 'guid'
    name = 'GUID'
    convert_value = True

class ValidFormat(ValidModelValue):
    class_ = 'Format'
    attr = 'name'
    name = 'name'
    convert_value = True

class ValidStyle(ValidModelValue):
    class_ = 'Style'
    attr = 'name'
    name = 'name'
    convert_value = True

class Range(validators.FancyValidator):
    messages = {
        'invalid': u"Invalid range."
    }

    def _to_python(self, value, state):
        parts = value.split(':', 1)
        try:
            if len(parts) > 1:
                return range(int(parts[0]), int(parts[1])+1)
            else:
                return [int(parts[0])]
        except ValueError, exc:
            raise validators.Invalid(self.message('invalid', state,
                value=value), value, state)

class SpamBayesFilter(validators.FancyValidator):
    """Check given value dict against SpamBayes xmlrpc server."""

    __unpackargs__ = ['error_field']

    sbrpc_url = 'http://localhost:8001/sbrpc'
    spam_threshold = 0.8
    default_score = 0.5

    messages = {
        'isSpam': u'Your form submission was rejected as spam.'
    }

    def validate_python(self, value, state):
        sbrpc_url = config.get('sbfilter.sbrpc_url', self.sbrpc_url)
        sb_proxy = xmlrpclib.ServerProxy(sbrpc_url, allow_none=True)
        try:
            score = sb_proxy.score(self.convert_values(value), [], [])
        except (socket.error, xmlrpclib.Error, TypeError), exc:
            log.warning("SpamBayes XmlRPC call to 'score()' on '%s' failed: %r",
                self.sbrpc_url, exc)
            score = self.default_score
        log.debug("SpamBayes score for value with keys %s: %.4f", value.keys(),
            score)
        if score >= self.spam_threshold:
            msg = self.message('isSpam', state, value=value, score=score)
            if self.error_field:
                error_dict = {self.error_field: msg}
            else:
                error_dict = None
            raise validators.Invalid(msg, value, state,
                error_dict=error_dict)

    def convert_values(self, values, state=None):
        if isinstance(values, dict):
            result = dict()
            for key, value in values.iteritems():
                if isinstance(value, dict) or hasattr(value, '__iter__'):
                    result[key] = convert_values(value)
                if type(value) not in xmlrpclib.Marshaller.dispatch.keys():
                    result[key] = jsonify(value)
                else:
                    result[key] = value
        elif hasattr(values, '__iter__'):
            result = []
            for value in values:
                if isinstance(value, dict) or hasattr(values, '__iter__'):
                    result.append(convert_values(value))
                elif type(value) not in xmlrpclib.Marshaller.dispatch.keys():
                    result.append(jsonify(value))
                else:
                    result.append(value)
        else:
            result = value
        return result
