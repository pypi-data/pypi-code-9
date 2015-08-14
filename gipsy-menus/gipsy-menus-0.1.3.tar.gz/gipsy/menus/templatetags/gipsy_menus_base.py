#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.template import Node, Variable


class MenuTagNode(Node):
    def __init__(self, model, stub, context_name=None):
        self.context_name = context_name
        self.stub = Variable(stub)
        self.model = model

    def render(self, context):
        stub = self.stub.resolve(context)

        try:
            menu_root = self.model.objects.get(stub=stub)
        except self.model.DoesNotExist:
            menu_root = None

        if self.context_name:
            context[self.context_name] = menu_root
            return ''
        else:
            raise Exception('not implemented yet')


def menu_tag(model, parser, token):
    """
    Render or return menu

    Syntax::

        {% menu <stub> [as <context_name>] %}

    """

    context_name = None
    bits = list(token.contents.split())
    if 'as' in bits:
        i = bits.index('as')
        bits.pop(i)
        context_name = bits.pop(i)

    return MenuTagNode(model, *bits[1:], context_name=context_name)
