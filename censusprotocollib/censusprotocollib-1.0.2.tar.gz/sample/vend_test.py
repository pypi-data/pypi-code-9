__author__ = 'lpreimesberger'
__copyright__ = 'copyright (c) 2015 census protocol foundation'
#
#
# this is part of the test suite - you are free to use  the software for any  purpose
# we welcome your donations - all are tax deductible and  go to education and pay for
# core  protocol  developers and  evangelists.  the sitting board receives no salary.

#  "You  have  to  find  a  way to earn your living without transgressing your ideals
#   of love and compassion" - Thich Nhat Hanh

#                          19MSTA2Zcuga7rTqLY5vfXLWDBkdfcVQ2U
#
#  if you require a tax receipt for your donation - send the txid to donate@censusprotocol.org
#
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Census Protocol Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a  copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the  rights
# to use, copy, modify, merge, publish,  distribute,  sublicense,  and/or  sell
# copies  of  the  Software,  and  to  permit persons to whom the  Software  is
# furnished to do so, subject to the following conditions:
#
# The  above copyright notice  and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE  SOFTWARE  IS PROVIDED "AS IS",  WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING  BUT  NOT LIMITED  TO  THE  WARRANTIES OF MERCHANTABILITY,
# FITNESS  FOR  A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS   OR  COPYRIGHT  HOLDERS  BE LIABLE  FOR ANY  CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR  OTHERWISE, ARISING FROM,
# OUT OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE USE  OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys
import time
import uuid
import json
import pybitcointools
import requests

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

from threading import Thread
# import the constants for this release
with open( '../server/server/census/v01-00.json') as data_file:
    census = json.load(data_file)
# python has a weird cfg format, using same as everything else
with open( 'config.json') as data_file:
    config = json.load(data_file)

json_data = {"version": 1,
               "item_type": "vend",
               "txid": "1",
               "created":"1",
               "block_in": "",
               "vend_item":"",
               "price":2000,
               "source": config['NODEWALLET'], #str(new_key.address),
               "expiration": "11/11/2015 20:00:00",
               "tips": 10,
               "signature": ""}

if len(sys.argv) != 2:
    print "Usage\npython vend_test.py <txid to sell>"
    sys,exit()

print sys.argv[1]
now_ms = lambda: int(round(time.time() * 1000))

max_loop = 4000
chunk_size = 1000
loop = 0
the_threads = []

start = now_ms()

def async(chunk):
    loop = 0
    while( loop < chunk ):
        json_data["signature"] = "";
        json_data["txid"] = str(uuid.uuid4())
        json_data["expiration"] = now_ms()+360000000;
        json_data["created"] = now_ms()+0;
        json_data["vend_item"] = sys.argv[1]
        # compute signature for the current key
        theString = json.dumps( json_data, sort_keys=True, separators=(',',':') )
        print "signing with [" + config['RAWPKEY'] + "]"
        signature = pybitcointools.ecdsa_sign( theString, config['RAWPKEY'] ) # new_key.pk )
        json_data["signature"] = str(signature)
        print json_data
        r = requests.post(
            "http://localhost:9000/api/v1/vend",
            headers=headers,
            data=json.dumps( json_data, sort_keys=True, separators=(',',':') )
        )
        print r.text
        loop = loop + 1


#while loop < max_loop :
#    thread = Thread( target = async, args = (chunk_size,) )
#    the_threads.append(thread)
#    thread.start()
#    loop = loop + chunk_size

#print "Waiting..."
# wait for all
#while len(the_threads):
#    wait_for_me = the_threads.pop();
#    wait_for_me.join()

async(1)
end = now_ms()

ms = end - start
print( str(max_loop) + " transactions in " + str(ms) + " milliseconds.")
seconds = ms / 1000.00000
tps = max_loop / seconds
print( "Observed TPS is about " + str(tps) )






