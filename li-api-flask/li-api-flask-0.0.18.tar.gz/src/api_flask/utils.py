# -*- coding: utf-8 -*-
import re
import json
from flask import request
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder


def limit(request):
    if request.args.get('limit', None):
        return int(request.args.get('limit'))
    return None


def offset(request):
    return int(request.args.get('offset', 0))


def order(request, queryset):
    order = request.args.get('order', '').lower()
    sort = request.args.get('sort', '')

    if sort and order and order in ['asc', 'desc']:
        return queryset.order_by('-{}'.format(sort) if order == 'desc' else sort)
    return queryset


def get_fields(request, fields):
    keys = request.args.get('fields', None)

    return dict((k, fields[k]) for k in keys.split(',') if k in fields) if keys else fields


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# Executa tarefas no celery
@static_vars(celery=None)
def doing_task(task_name, option='delay', args=None):

    # Conecta no celery
    if doing_task.celery is None:
        BROKER_URL = "redis://" + settings.REDIS['HOST'] + ':' + settings.REDIS['PORT'] + '/' + settings.REDIS['DB']
        BACKEND_URL = BROKER_URL
        celery = Celery('DOING', broker=BROKER_URL, backend=BACKEND_URL)

    try:
        if args is not None:
            data = args
        elif request.data:
            try:
                data = json.loads(request.data)
            except:
                data = request.data
        elif request.form:
            data = dict([(k, v[0] if len(v) == 1 else v) for k, v in dict(request.form).items()])
        else:
            data = None

        if not data:
            return 'No data'

        # print(u"Enviando para o celery atraves do broker {} com data = {}".format(celery.conf.BROKER_URL, data))
        if option == 'get':
            celery_response = celery.signature(task_name, kwargs=data).delay().get(timeout=60)
            # print("Recebido do celery!")
            data = json.dumps(celery_response)

            return data
        else:
            celery_response = celery.signature(task_name, kwargs=data).delay()

        if celery_response.status == 'SUCCESS' or celery_response.status == 'PENDING':
            return { 'status': 'SUCCESS', 'code': 200 }
        else:
            return { 'status': 'ERROR', 'code': 500 }

    except TimeoutError:
        return { 'status': 'TIMEOUT', 'code': 408 }


class FlatJsonSerializer(Serializer):
    def get_dump_object(self, obj):
        data = self._current
        if not self.selected_fields or 'id' in self.selected_fields:
            data['id'] = obj.id
        return data
    def end_object(self, obj):
        if not self.first:
            self.stream.write(', ')
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder)
        self._current = None
    def start_serialization(self):
        self.stream.write("[")
    def end_serialization(self):
        self.stream.write("]")
    def getvalue(self):
        return super(Serializer, self).getvalue()


def response_format(data):
    object = request.args.get('object',None)

    if object == 'true':
        data = { 'data': data }

    return data


# TODO: Funcao de validacao de tados da API
def validar_tipo_pessoa(json, errors, data):

    if str(data) == "PF":
        if json.get('cpf') in (None, ''):
            errors.append({'field': 'cpf', 'message': None})

    elif data == "PJ":
        if json.get('cnpj') in (None,''):
            errors.append({'field': 'cnpj', 'message': None})
        if json.get('razao_social') in (None,''):
            errors.append({'field': 'razao_social', 'message': None})

    else:
        return False

    return True


def validar_email(json, errors, data):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", str(data)):
        return True
    else:
        return False


def validar_telefone (json, errors, data):
    if data is None:
        return True

    if re.match("^[0-9]{10,11}$",str(data)):
        return True
    else:
        return False


def validar_forma_pagamento(json, errors, data):
    if re.match("^(BOLETO|CARTAO DE CREDITO)$",str(data)):
        return True
    else:
        return False


def validar_cep(json, errors, data):
    if re.match("^[0-9]{8}$",str(data)):
        return True
    else:
        return False


# TODO: Confirmar se o código existe
def validar_cidade_ibge(json, errors, data):
    if re.match("^[0-9]{7}$",str(data)):
        return True
    else:
        return False


def validar_estado(json, errors, data):
    estados = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA",
               "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]

    if str(data) in estados:
        return True
    else:
        return False


def validar_cartao_de_credito_numero(json, errors, data):
    if re.match("^[0-9]{13,19}$",str(data)):
        return True
    else:
        return False


def validar_cartao_de_credito_cvv(json, errors, data):
    if re.match("^[0-9]{3,4}$",str(data)):
        return True
    else:
        return False


def validar_cartao_de_credito_expiracao_mes(json, errors, data):
    if re.match("^[0-9]{2}$",str(data)):
        return True
    else:
        return False


def validar_cartao_de_credito_expiracao_ano(json, errors, data):
    if re.match("^[0-9]{2}$",str(data)):
        return True
    else:
        return False
