import datetime
from tempfile import NamedTemporaryFile

from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.humanize.templatetags.humanize import naturaltime

import json


UTC = datetime.datetime.utcnow


class JorjunJSONEncoder(DjangoJSONEncoder):
    """
    JSON needs to know how to deal with BSON Object ID data type:
    mainly the _id field in a mongo collection
    """
    def default(self, o):
        if o.__class__.__name__== 'ObjectId':
            return str(o)
        else:
            return super(JorjunJSONEncoder, self).default(o)

    def json_encode(self, obj):
        return django_json_encoder.encode(obj)


class JSONResponseMixin(object):
    def render_to_response(self, context):
        def _get_json_response(content, **httpresponse_kwargs):
            return http.HttpResponse(content,
                                     content_type='application/json',
                                     **httpresponse_kwargs)
        def _convert_context_to_json(context):
            return django_json_encoder.json_encode(context)

        return _get_json_response(_convert_context_to_json(context))


django_json_encoder =   JorjunJSONEncoder(ensure_ascii=False, indent=4)


def from_timestamp(ts):
    if ts:
        return datetime.datetime.fromtimestamp(int(ts))
    else:
        return None


def make_temp_file(suffix, delete=False):
    """
    """
    tempf = NamedTemporaryFile(suffix=suffix, delete=delete)
    path = tempf.name
    #tempf.close()
    return path


def make_token(token_length=7):
    """
    Create unique token reference
    """
    while True:
        token = ''.join(
            [choice(self.CHARS) for xx in range(token_length)]
        )
        doc = self.find_one({"token": token})
        if not doc:
            break

    doc = {
        "token": token,
        "expire_utc": UTC() + datetime.timedelta(hours=settings.TOKEN_EXPIRE_HOURS),
    }
    _id = self.insert(doc)
    assert _id, "Problem creating token"
    return doc
