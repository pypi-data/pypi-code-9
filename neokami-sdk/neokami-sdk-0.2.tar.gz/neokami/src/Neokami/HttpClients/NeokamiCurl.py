''' Copyright 2015 Neokami GmbH. '''

import requests


class NeokamiHttpClient():


    def get(self, route, payload):
        r = requests.get(route, params=payload)

        return r

    def post(self, route, api_key, payload):
        headers = {'apikey': api_key }
        r = requests.post(route, data=payload, headers=headers)
        return r

    def postBinary(self, route, bytestream, api_key, params={}):
        '''
        :param route:
        :param bytestream:
        :param api_key:
        :param params:
        :return:
        '''


        headers = {'apikey': api_key }
        files = {'data':bytestream}
        r = requests.post(
                    url=route,
                    data=params,
                    files=files,
                    headers=headers)

        return r

