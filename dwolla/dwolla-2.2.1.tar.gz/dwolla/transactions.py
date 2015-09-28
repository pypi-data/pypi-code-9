'''
      _               _ _
   __| |_      _____ | | | __ _
  / _` \ \ /\ / / _ \| | |/ _` |
 | (_| |\ V  V / (_) | | | (_| |
  \__,_| \_/\_/ \___/|_|_|\__,_|

  An official requests based wrapper for the Dwolla API.

  This file contains functionality for all transactions related endpoints.
'''

from . import constants as c
from .rest import r


def send(destinationid, amount, **kwargs):
    """
    Sends money to the specified destination user.

    :param destinationid: String of Dwolla ID to send funds to.
    :param amount: Double of amount to sen
    :param params: Dictionary of additional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Integer of transaction ID
    """
    if not destinationid:
        raise Exception('send() requires destinationid parameter')
    if not amount:
        raise Exception('send() requires amount parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin),
        'destinationId': destinationid,
        'amount': amount
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/transactions/send', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def get(**kwargs):
    """
    Lists transactions for the user associated with
    the currently set OAuth token.

    :param params: Dictionary with additional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with transactions
    """
    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'client_id': kwargs.pop('client_id', c.client_id),
        'client_secret': kwargs.pop('client_secret', c.client_secret)
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/transactions', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def info(tid, **kwargs):
    """
    Returns transaction information for the transaction
    associated with the passed transaction ID

    :param id: String with transaction ID.

    :param kwargs: Additional parameters for client control.

    :return: Dictionary with information about transaction.
    """
    if not tid:
        raise Exception('info() requires id parameter')

    return r._get('/transactions/' + tid,
                  {
                      'oauth_token': kwargs.pop('alternate_token', c.access_token),
                      'client_id': kwargs.pop('client_id', c.client_id),
                      'client_secret': kwargs.pop('client_secret', c.client_secret)
                  }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))


def refund(tid, fundingsource, amount, **kwargs):
    """
    Refunds (either completely or partially) funds to
    the sending user for a transaction.

    :param id: String with transaction ID.
    :param fundingsource: String with funding source for refund transaction.
    :param amount: Double with amount to refun
    :param params: Dictionary with additional parameters.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with information about refund transaction.
    """
    if not tid:
        raise Exception('refund() requires parameter id')
    if not fundingsource:
        raise Exception('refund() requires parameter fundingsource')
    if not amount:
        raise Exception('refund() requires parameter amount')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin),
        'fundsSource': fundingsource,
        'transactionId': tid,
        'amount': amount
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/transactions/refund', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def stats(**kwargs):
    """
    Retrieves transaction statistics for
    the user associated with the current OAuth token.

    :param params: Dictionary with additional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with transaction statistics
    """
    p = {'oauth_token': kwargs.pop('alternate_token', c.access_token)}

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/transactions/stats', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))

def schedule(destinationid, amount, scheduledate, fundssource, **kwargs):
    """
    Sends money to the specified destination user.

    :param destinationid: String of Dwolla ID to send funds to.
    :param amount: Double of amount to sen
    :param scheduledate: YYYY-MM-DD format date for when to send funds.
    :param fundssource: Funding source ID to fund scheduled transaction
    :param params: Dictionary of additional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Integer of transaction ID
    """
    if not destinationid:
        raise Exception('schedule() requires destinationid parameter')
    if not amount:
        raise Exception('schedule() requires amount parameter')
    if not scheduledate:
        raise Exception('schedule() requires scheduledate parameter')
    if not fundssource:
        raise Exception('schedule() requires fundssource parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin),
        'destinationId': destinationid,
        'amount': amount,
        'scheduleDate': scheduledate,
        'fundsSource': fundssource
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/transactions/scheduled', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))

def scheduled(**kwargs):
    """
    Retrieves all scheduled transactions

    :param params: Dictionary of additional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: List of scheduled transactions
    """
    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token)
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/transactions/scheduled', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))

def scheduledbyid(tid, **kwargs):
    """
    Retrieve scheduled transaction by ID

    :param tid: Scheduled transaction ID

    :param kwargs: Additional parameters for client control.

    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('scheduledbyid() requires tid parameter')

    return r._get('/transactions/scheduled/' + tid, 
        {
            'oauth_token': kwargs.pop('alternate_token', c.access_token)
        }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))

def editscheduledbyid(tid, **kwargs):
    """
    Edit scheduled transaction by ID

    :param tid: Scheduled transaction ID
    :param params: Dictionary of additional parameters

    :param kwargs: Additional parameters for client control.

    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('editscheduledbyid() requires tid parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin)
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._put('/transactions/scheduled/' + tid, p, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))

def deletescheduledbyid(tid, **kwargs):
    """
    Delete scheduled transaction by ID

    :param tid: Scheduled transaction ID

    :param kwargs: Additional parameters for client control.

    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('scheduledbyid() requires tid parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin)
    }

    return r._delete('/transactions/scheduled/' + tid, p, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))

def deleteallscheduled(**kwargs):
    """
    Delete all scheduled transactions

    :param kwargs: Additional parameters for client control.
    
    :return: Requested scheduled transaction
    """

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin)
    }

    return r._delete('/transactions/scheduled', p, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))