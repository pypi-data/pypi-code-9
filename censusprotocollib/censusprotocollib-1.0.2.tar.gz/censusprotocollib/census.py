__author__ = 'census protocol foundation'
import urllib2
import time
import json
import pybitcointools
import requests


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
now_ms = lambda: int(round(time.time() * 1000))
serialize = lambda json_data: json.dumps( json_data, sort_keys=True, separators=(',',':') )

def generate_wallet( my_seed_data ):
    """ create a new empty wallet - does not post it.  this is a VERY EXPENSIVE operation
    :param my_seed_data: seed for the wallet - this should be a big random block, but as always...
    :return: object containing, public, private, and address info
    """
    new_wallet = {}
    hash_of_seed = pybitcointools.sha256(my_seed_data)
    new_wallet["public"] = pybitcointools.privkey_to_pubkey(hash_of_seed)
    new_wallet["private"] = hash_of_seed;
    new_wallet["address"] = pybitcointools.pubtoaddr( new_wallet["public"])
    return new_wallet

def version( host ):
    """ get the version block from the given server
    :param host: host to connect to
    :return: json data for that host or raises exception
    """
    url = 'http://{}:9000/api/v1/version'.format(host)
    # let it throw exception on fail and bubble up
    return urllib2.urlopen(url).read()


def sign( json_data, private_key ):
    """ sign the json info - returning the json object modified
    :param json_data: what to sign
    :param private_key: ecdsa key to use
    :return: updated json_data.  signature replaced with new signature
    """
    # clear if present
    json_data['signature'] = ""
    # sort and normalize the json data
    theString = json.dumps( json_data, sort_keys=True, separators=(',',':') )
    print "signing\n" + theString
    signature = pybitcointools.ecdsa_sign( theString, private_key )
    json_data['signature'] = signature
    print "signed!!!"
    print json_data
    print "signed!!!"
    return json_data


def check( json_data, public_key ):
    """ implementing the bitcoin.message.sign using the address is horrible in python
    i linked in a tiny library in crypto from electrum - but the bitcoin way assumes you
    only can add 255 bytes to the message since there's a pascal-style string at the front.
    this requires a wallet PUBLIC KEY - the web client is happy with the address
    :param json_data: data to check
    :param public_key: ecdsa encoded PUBLIC KEY - not the address
    :return: true or false
    """
    # clear if present
    the_signature = json_data['signature']
    json_data['signature'] = ""
    # sort and normalize the json data
    theString = json.dumps( json_data, sort_keys=True, separators=(',',':') )
    is_okay = pybitcointools.ecdsa_verify( theString, the_signature, public_key )
    return is_okay


def vend( host, json_data ):
    """ send this json to the host as a vend transaction
    :param host: host to connect to
    :param json_data: data to send.  must be signed
    :return: server response - normally json
    """
    r = requests.post(
        "http://{}:9000/api/v1/vend".format(host),
        headers=headers,
        data=serialize(json_data)
    )
    return r.text

def item( host, json_data ):
    """ send this json to the host as a item transaction
    :param host: host to connect to
    :param json_data: data to send.  must be signed
    :return: server response - normally json
    """
    r = requests.post(
        "http://{}:9000/api/v1/item".format(host),
        headers=headers,
        data=serialize(json_data)
    )
    return r.text

def items_from_venue( host, venue ):
    """ find items from this venue - capped, but at least 50
    :param host: host to connect to
    :param json_data: data to send.  must be signed
    :return: server response - normally json
    """
    r = requests.get(
        "http://{}:9000/api/v1/item/venue/{}".format(host, venue),
        headers=headers

    )
    return r.text

def items_from_location( host, lat, lon, distance_km ):
    """ get items around a certain point
    :param host:
    :param lat: latitude
    :param lon: longitude
    :param distance_km: how far away in km
    :return: listing
    """
    r = requests.get(
        "http://{}:9000/api/v1/item/geo/{}/{}/{}".format(host, lat, lon, distance_km),
        headers=headers

    )
    return r.text

def get_item( host, txid ):
    """ returns current state for this item
    :param host: host to connect to
    :param txid: data to send.  must be signed
    :return: server response - normally json
    """
    r = requests.get(
        "http://{}:9000/api/v1/item/{}".format(host, txid ),
        headers=headers

    )
    return r.text



def buy( host, json_data ):
    """ send this json to the host as a buy transaction
    :param host: host to connect to
    :param json_data: data to send.  must be signed
    :return: server response - normally json
    """
    r = requests.post(
        "http://{}:9000/api/v1/buy".format(host),
        headers=headers,
        data=serialize(json_data)
    )
    return r.text


def wallet( host, wallet_id ):
    """ send this json to the host as a wallet create transaction
    :param host: host to connect to
    :param wallet_id: the wallet uuid
    :return: server response - normally json
    """
    r = requests.post(
        "http://{}:9000/api/v1/wallet/{}".format(host. wallet_id ),
        headers=headers,
        data=serialize(json_data)
    )
    return r.text

def get_wallet( host, wallet_id ):
    """ get the information for a given wallet
    :param host: host to connect to
    :param wallet_id: the wallet uuid
    :return: server response - normally json
    """
    r = requests.get(
        "http://{}:9000/api/v1/wallet/{}".format(host, wallet_id),
        headers=headers
    )
    return r.text

def get_owned_items( host, wallet_id ):
    """ get the items owned by this user
    :param host: host to connect to
    :param wallet_id: the wallet uuid
    :return: server response - normally json
    """
    r = requests.get(
        "http://{}:9000/api/v1/wallet/owned/{}".format(host, wallet_id),
        headers=headers
    )
    return r.text
