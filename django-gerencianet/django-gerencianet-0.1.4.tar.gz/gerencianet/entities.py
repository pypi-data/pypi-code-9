#!/usr/bin/python
# -*- encoding: utf-8 -*-


class GatewayPayment(object):

    def __init__(self, identifier, transaction, link):
        self.identifier = identifier
        self.transaction = transaction
        self.link = link

    def __repr__(self):
        return self.identifier + '-' + str(self.transaction) + ' - ' + str(self.link)


class GatewayPlan(object):

    def __init__(self, code, value, description, periodicity, recurrent, credits_app=None):
        self.code = code
        self.value = value
        self.description = description
        self.periodicity = periodicity
        self.recurrent = recurrent
        self.credits_app = credits_app

    def __repr__(self):
        return str(self.code) + ' - ' + str(self.value) + ' - ' + str(self.description)


class GatewayTransactionHistory(object):

    def __init__(self, action, date, status):
        self.action = action
        self.date = date
        self.status = status

    def __repr__(self):
        return self.action.encode("utf-8") + ' - ' + str(self.date) + ' - ' + str(self.status)


class GatewayInformation(object):

    def __init__(self, transaction, identifier, history=None):
        self.transaction = transaction
        self.identifier = identifier
        self.history = history

    def __repr__(self):
        return str(self.identifier) + '-' + str(self.transaction) + '-' + str(self.history)