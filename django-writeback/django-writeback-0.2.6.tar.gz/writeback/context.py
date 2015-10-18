# -*- coding: utf-8 -*-

from writeback.views import MessageCreateForm


def add_form(request):
    return {
        'writeback_form': MessageCreateForm(),
    }