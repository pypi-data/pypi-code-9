# -*- coding: utf-8 -*-
import os
import autenticacao_api


autenticacao = autenticacao_api.autenticacao()
autenticacao.define_valor("chave_aplicacao", os.environ.get('CHAVE_API'))