# #encoding:utf-8
# from celery import task
from .modulos.saldos_clientes.core import formar_correo


# @task
def enviar_correo(**kwargs):
    formar_correo(kwargs=kwargs)
