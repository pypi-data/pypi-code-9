#!/usr/bin/python
# -*- encoding: utf-8 -*-

import requests
import simplejson
from gerencianet.constants import GatewayStatusResponse
from gerencianet.exceptions import GatewayGerenciaNetError


def do_gateway_post(url, data, headers=None):
    http_response = requests.post(url, data=data, headers=headers)
    gateway_response = simplejson.loads(http_response.content)
    if gateway_response['status'] == GatewayStatusResponse.error:
        raise GatewayGerenciaNetError(gateway_response['erros'])

    return gateway_response