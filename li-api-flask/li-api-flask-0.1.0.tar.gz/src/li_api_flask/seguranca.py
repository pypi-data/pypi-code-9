# -*- coding: utf-8 -*-
from li_api_flask import restful


def autenticacao(nome_api=None, versao_api=None):
    return restful.Autenticacao(nome_api, versao_api)