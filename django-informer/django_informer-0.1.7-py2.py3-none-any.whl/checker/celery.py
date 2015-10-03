# coding: utf-8

"""django informer checker for Celery"""

from __future__ import absolute_import

from informer.checker.base import BaseInformer, InformerException


class CeleryInformer(BaseInformer):
    """
    Celery Informer.
    """

    def __str__(self):
        return u'Check if Celery is operational.'

    def check(self):
        """
        Perform check against default Celery configuration
        """
        try:
            from celery.task.control import inspect

            ins = inspect()
            stats = ins.stats()

            if not stats:
                return False, 'No running Celery workers were found.'
        except ImportError as error:
            raise InformerException(
                'Celery is not installed: %s' % error)
        except IOError as error:
            raise InformerException(
                'Error connecting to the backend: %s' % error)
        except Exception as error:
            raise InformerException(
                'An error occured when trying use Celery: %s.' % error)
        else:
            return True, 'Celery is operational.'
