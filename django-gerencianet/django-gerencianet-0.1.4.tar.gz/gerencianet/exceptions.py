#!/usr/bin/python
# -*- encoding: utf-8 -*-


class GatewayGerenciaNetError(Exception):

    def __init__(self, errors):
        code = errors.get('codigo')
        error = errors.get('erro')
        if error:
            error = error.encode('utf-8')
        message = "codigo: {0} - mensagem: {1}".format(code, error)
        super(GatewayGerenciaNetError, self).__init__(message)
