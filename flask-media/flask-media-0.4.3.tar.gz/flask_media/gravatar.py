# coding: utf-8
import hashlib
from flask import request

__all__ = (
    'format_gravatar',
    'gravatar_hash'
)

__author__ = 'vadim'


def format_gravatar(user_hash, size=None, default=None, rating=None):
    """
    Return url to gravatar
    :param size: image size? in pixels. Default: 32
    :param default: The default image generator for users who have no avatars registered with the Gravatar service.
                    Options are "404" to return a 404 error, a URL that points to a default image, or one of the
                    following image generators: "mm", "identicon", "monsterid", "wavatar", "retro", or "blank".
                    Default: "identicon"
    :param rating: Image rating. Options are "g", "pg", "r", and "x". Default: "g"
    :return: url to gravatar
    """
    size = size or 32
    default = default or 'identicon'
    rating = rating or 'g'
    url = 'https://secure.' if request.is_secure else 'http://www.'
    url += 'gravatar.com/avatar'

    return '{url}/{hash}?s={size}&d={default}&r={rating}'.\
        format(url=url, hash=user_hash, size=size, default=default, rating=rating)

gravatar_hash = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()
