# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Paper
# Copyright 2015 ActivKonnect

from django.db.models import signals


def listen_to_model(model, finder, name, calc):
    to_handle = []

    # noinspection PyUnusedLocal
    def post_save_handler(instance, **kwargs):
        for obj in finder(instance):
            setattr(obj, name, calc(obj))
            obj.save()

    # noinspection PyUnusedLocal
    def pre_delete_handler(instance, **kwargs):
        to_handle.extend(finder(instance))

    # noinspection PyUnusedLocal
    def post_delete_handler(**kwargs):
        for obj in to_handle:
            setattr(obj, name, calc(obj))
            obj.save()
        del to_handle[:]

    signals.post_save.connect(post_save_handler, sender=model, weak=False)
    signals.pre_delete.connect(pre_delete_handler, sender=model, weak=False)
    signals.post_delete.connect(post_delete_handler, sender=model, weak=False)


def cardboard(field, dependencies):
    def decorator(func):
        for model, finder in dependencies:
            listen_to_model(model, finder, func.__name__, func)

        return field
    return decorator
