# -*- coding:utf-8 -*-

import urllib
import requests
from contextlib import contextmanager

from .anti_config import db


@contextmanager
def transaction():
    db.session.begin(nested=db.session.is_active)
    try:
        yield
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()


def dict_of_array(arr, model, field):
    """ Создание новых элементов, на выходе словарь {field:id} """
    res = db.session.query(getattr(model, field)).filter(getattr(model, field).in_(arr)).all()
    res = [item[0] for item in res]
    [db.session.add(model(**{field: item})) for item in arr if item not in res and item]
    db.session.commit()
    data = db.session.query(getattr(model, field), getattr(model, 'id')).filter(getattr(model, field).in_(arr)).all()
    data = {item: item_id for item, item_id in data}
    return data


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_normal_url(url):
    url = url.strip().lower().replace('http://', '').replace('https://', '').replace('www.', '')
    if len(url) > 0:
        if url[-1] == '/':
            url = url[:-1]
        if len(url) < 20:
            url = url.encode('idna')
        return url[:255]
    return None


def get_normal_url_decode(url):
    url = url.strip().lower().replace('http://', '').replace('https://', '').replace('www.', '')
    if len(url) > 0:
        if url[-1] == '/':
            url = url[:-1]
        try:
            url = url.decode('idna')
        except:
            pass
        return url[:255]
    return None


def GetHash(query):
    SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
    Result = 0x01020345
    for i in range(len(query)):
        Result ^= ord(SEED[i % len(SEED)]) ^ ord(query[i])
        Result = Result >> 23 | Result << 9
        Result &= 0xffffffff
    return '8%x' % Result


def check_page(url):
    try:
        resp = requests.get('http://' + url, verify=False)
    except:
        try:
            resp = requests.get('http://www.' + url, verify=False)
        except:
            return False

    if resp.status_code == 200:
        return resp.text
    return False


def check_absolute_page(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return True
    except:
        pass
    return False


def remove_last_slash(link):
    if len(link) > 0:
        if link[-1] == '/':
            link = link[:-1]
    return link


def get_normal_quote(phrase):
    phrase = phrase.lower().strip()
    if isinstance(phrase, unicode):
        phrase_quote = urllib.quote_plus(phrase.encode('utf8'))
    else:
        phrase_quote = urllib.quote_plus(phrase)
    return phrase_quote
