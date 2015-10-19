#!/usr/bin/python
# -*- encoding: utf-8 -*-
from gerencianet.constants import GatewayStatusResponse
from gerencianet.models import PaymentLog


def insert_success_log(notification, email=None, response=None, identifier=None):
    PaymentLog.objects.create(
        data=notification, email=email, identifier=identifier, response=response, status=GatewayStatusResponse.success)


def insert_error_log(notification, email=None, response=None, identifier=None):
    PaymentLog.objects.create(
        data=notification, email=email, identifier=identifier, response=response, status=GatewayStatusResponse.error)
