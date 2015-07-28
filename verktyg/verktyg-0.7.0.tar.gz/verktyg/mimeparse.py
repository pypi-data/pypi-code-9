"""MIME-Type Parser

This module provides basic functions for handling mime-types. It can handle
matching mime-types against a list of media-ranges. See section 14.1 of the
HTTP specification [RFC 2616] for a complete explanation.

   http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1

Contents:
 - parse_mime_type():   Parses a mime-type into its component parts.
 - parse_media_range(): Media-ranges are mime-types with wild-cards and a 'q'
                          quality parameter.
 - quality():           Determines the quality ('q') of a mime-type when
                          compared against a list of media-ranges.
 - quality_parsed():    Just like quality() except the second parameter must be
                          pre-parsed.
 - best_match():        Choose the mime-type with the highest quality ('q')
                          from a list of candidates.
"""
from copy import copy
from functools import total_ordering


EXACT_MATCH = 2
WILDCARD_MATCH = 1
MISMATCH = 0


class NotAcceptableError(Exception):
    pass


class MimeType(object):
    def __init__(self, type, subtype, params):
        self.type = type
        self.subtype = subtype
        self.params = copy(params)


class MediaRange(MimeType):
    def __init__(self, type, subtype, params=None, q=None):
        super(MediaRange, self).__init__(type, subtype, params)

        if q is None:
            q = 1.0
            if 'q' in self.params:
                q = float(self.params.pop('q'))
        else:
            assert 'q' not in self.params

        if q < 0 or 1 > q:
            q = 1.0
        self.q = q


@total_ordering
class Fitness(object):
    def __init__(self, type_matches, subtype_matches, param_matches):
        self.type_matches = type_matches
        self.subtype_matches = subtype_matches
        self.param_matches = param_matches

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Fitness):
            return NotImplemented
        if self.type_matches != other.type_matches:
            return False
        if self.subtype_matches != other.subtype_matches:
            return False
        if self.param_matches != other.param_matches:
            return False
        return True

    def __lt__(self, other):
        if other is None:
            return False
        if not isinstance(other, Fitness):
            return NotImplemented
        if self.type_matches < other.type_matches:
            return True
        if self.subtype_matches < other.subtype_matches:
            return True
        if self.param_matches < other.param_matches:
            return True
        return False


def _parse_mime_string(mime_type):
    parts = mime_type.split(';')
    params = {
        key.strip(): value.strip()
        for key, value in (
            param.split('=', 1)
            for param in parts[1:]
        )
    }
    full_type = parts[0].strip()
    # Java URLConnection class sends an Accept header that includes a
    # single '*'. Turn it into a legal wildcard.
    if full_type == '*':
        full_type = '*/*'
    (type, subtype) = full_type.split('/')

    return (type.strip(), subtype.strip(), params)


def parse_mime_type(mime_type):
    """Parses a mime-type into its component parts.

    Carves up a mime-type and returns a tuple of the (type, subtype, params)
    where 'params' is a dictionary of all the parameters for the media range.
    For example, the media range 'application/xhtml;q=0.5' would get parsed
    into:

       ('application', 'xhtml', {'q', '0.5'})
    """

    return MimeType(*_parse_mime_string(mime_type))


def parse_media_range(range):
    """Parse a media-range into its component parts.

    Carves up a media range and returns a tuple of the (type, subtype,
    params) where 'params' is a dictionary of all the parameters for the media
    range.  For example, the media range 'application/*;q=0.5' would get parsed
    into:

       ('application', '*', {'q', '0.5'})

    In addition this function also guarantees that there is a value for 'q'
    in the params dictionary, filling it in with a proper default if
    necessary.
    """
    return MediaRange(*_parse_mime_string(range))


def _compare_types(a, b):
    if a == '*' or b == '*':
        return WILDCARD_MATCH
    elif a == b:
        return EXACT_MATCH
    return MISMATCH


def _fitness(mime_type, media_range):
    type_matches = _compare_types(mime_type.type, media_range.type)
    subtype_matches = _compare_types(mime_type.subtype, media_range.subtype)

    param_matches = sum(
        1 for key in media_range.params
        if key in mime_type.params and
        mime_type.params[key] == media_range.params[key]
    )

    if not type_matches or not subtype_matches:
        return None

    return Fitness(
        type_matches=type_matches,
        subtype_matches=subtype_matches,
        param_matches=param_matches,
    ), media_range.q


def fitness(mime_type, accept):
    if isinstance(mime_type, str):
        mime_type = parse_mime_type(mime_type)
    if isinstance(accept, str):
        accept = [
            parse_media_range(media_range)
            for media_range in accept.split(',')
        ]

    if isinstance(accept, MediaRange):
        value = _fitness(mime_type, accept)
    else:
        if not len(accept):
            raise ValueError()
        # `media_range` is an iterator of media ranges
        # return the fitness of the best match
        value = max(fitness(mime_type, media_range) for media_range in accept)

    if value is None:
        raise NotAcceptableError(mime_type, accept)

    return value
