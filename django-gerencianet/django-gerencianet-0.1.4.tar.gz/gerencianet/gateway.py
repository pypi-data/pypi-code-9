#!/usr/bin/python
# -*- encoding: utf-8 -*-

from django.utils.datetime_safe import datetime
from django.conf import settings
import simplejson

from gerencianet.entities import GatewayInformation, GatewayPayment, GatewayTransactionHistory
from gerencianet.exceptions import GatewayGerenciaNetError
from gerencianet.repository import insert_success_log, insert_error_log
from gerencianet.services import do_gateway_post


def get_payment_link(email, plan, identifier=None, redirect_url=settings.GERENCIANET_REDIRECT_URL):
    timestamp = datetime.now().microsecond

    if identifier is None:
        identifier = '{0};{1};{2}'.format(email, plan.code, timestamp)

    items = list()
    value = int(("%.2f" % plan.value).replace('.', ''))
    items.append(dict(itemValor=value, itemDescricao=plan.description))

    data = dict(
        itens=items, periodicidade=plan.periodicity, cliente=dict(email=email),
        retorno=dict(urlNotificacao=settings.GERENCIANET_NOTIFICATION_URL,
                     url=redirect_url, identificador=identifier),
    )

    url_payment = settings.GERENCIANET_PAYMENT_URL
    if plan.recurrent is True:
        url_payment = settings.GERENCIANET_RECURRENT_PAYMENT_URL

    post_headers = {'content-type': 'application/x-www-form-urlencoded'}
    data_json = simplejson.dumps(data)
    post_data = dict(token=settings.GERENCIANET_TOKEN, dados=data_json)
    gateway_response = do_gateway_post(url_payment, post_data, post_headers)
    transaction = gateway_response['resposta']['transacao']
    link = gateway_response['resposta']['link']

    return GatewayPayment(identifier, transaction, link)


def get_notification_info(notification):
    data = simplejson.dumps(dict(notificacao=notification))
    post_headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_data = dict(token=settings.GERENCIANET_TOKEN, dados=data)
    url = settings.GERENCIANET_NOTIFICATION_INFO_URL

    try:
        gateway_response = do_gateway_post(url, post_data, post_headers)
        insert_success_log(notification, None, gateway_response, gateway_response['resposta'].get('identificador'))

        identifier = gateway_response['resposta'].get('identificador')
        transaction = gateway_response['resposta'].get('transacao')

        history = list()
        for h in gateway_response['resposta']['historico']:
            action = h['acao']
            date = h['data']
            status_h = h['codigoStatus']
            history.append(GatewayTransactionHistory(action, date, status_h))

        return GatewayInformation(transaction, identifier, history)

    except GatewayGerenciaNetError as gge:
        insert_error_log(notification, None, {"message": gge.message}, None)
        return None


