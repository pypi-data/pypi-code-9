# -*- coding: utf-8 -*-

"""
Funções para auxiliarem no desenvolvimento
"""

import os
import re
import time

from unicodedata import normalize
from functools import wraps
from .conexoes.worker import WorkerConnect

import logging
LOGGER = logging.getLogger()


def tente_outra_vez(excecoes, tentativas=4, tempo_espera=3, multiplicador_espera=1):
    """
    Escuta pelas exceções especificadas e refaz a chamada para o método.
    :param excecoes: As exceções que devem ser escutadas
    :type excecoes: Exception or tuple
    :param tentativas: Número de vezes que deve ser chamado o método
    :type tentativas: int
    :param tempo_espera: Tempo inicial de espera em segundos entre as tentativas
    :type tempo_espera: int
    :param multiplicador_espera: Multiplicador para o tempo de espera nas chamadas subsequentes.
    :type multiplicador_espera: int
    """
    def deco_tente_outra_vez(funcao):
        """
        Decorator para tente_outra_vez
        """
        @wraps(funcao)
        def funcao_tente_outra_vez(*args, **kwargs):
            """
            Tratamento de decorator para tente_outra_vez
            """
            _tentativas, _tempo_espera = tentativas, tempo_espera
            while _tentativas > 1:
                try:
                    return funcao(*args, **kwargs)
                except excecoes, exc:
                    msg = "{}, Reconectando in {} segundos...".format(str(exc), _tempo_espera)
                    if LOGGER:
                        LOGGER.warning(msg)
                    time.sleep(_tempo_espera)
                    _tentativas -= 1
                    _tempo_espera *= multiplicador_espera
            return funcao(*args, **kwargs)
        return funcao_tente_outra_vez
    return deco_tente_outra_vez


def remover_acentos(value):
    """Normalize the values."""
    try:
        return normalize('NFKD', value.decode('utf-8')).encode('ASCII', 'ignore')
    except UnicodeEncodeError:
        return normalize('NFKD', value).encode('ASCII', 'ignore')


def pegar_versao_git():
    """
    pegar_versao_git
    :return: git version
    """
    import subprocess

    try:
        version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        version = version.replace("\n","")
        return version
    except subprocess.CalledProcessError:
        return '0'


def send_email(template_file=None, context=None,
               contrato_id=None, conta_id=None, usuario_id=None, cliente_id=None, pedido_venda_id=None,
               salva_evidencia=True, to_email=None, reply_to=None, countdown=0):
    """
    send_email
    :param template_file: template_file
    :param context: context
    :param contrato_id: contrato_id
    :param conta_id: conta_id
    :param usuario_id: usuario_id
    :param cliente_id: cliente_id
    :param pedido_venda_id: pedido_venda_id
    :param salva_evidencia: salva_evidencia
    :param to_email: to_email
    :return: None
    """

    args = {
        "template_file": template_file,
        "context": context,
        "contrato_id": contrato_id,
        "conta_id": conta_id,
        "usuario_id": usuario_id,
        "cliente_id": cliente_id,
        "pedido_venda_id": pedido_venda_id,
        "salva_evidencia": salva_evidencia,
        "to_email": to_email,
        "reply_to": reply_to
    }

    WorkerConnect().execute('async.utils.send_email_template', args=args, countdown=countdown)


def send_email_sem_template(from_email=None, to_email=None, reply_to=None, subject=None,
            html_message=None, text_message=None, countdown=0, salva_evidencia=True
):
    """
    send_email_sem_template
    :param from_email: from_email
    :param to_email: to_email
    :param reply_to: reply_to
    :param subject: subject
    :param content: content
    :param countdown: countdown
    :return: None
    """

    args = {
        "from_email": from_email,
        "to_email": to_email,
        "reply_to": reply_to,
        "subject": subject,
        "html_message": html_message,
        "text_message": text_message,
        "salva_evidencia": salva_evidencia
    }

    WorkerConnect().execute('async.utils.send_email', args=args, countdown=countdown)


def carregar_env():
    files = ['/etc/profile.d/env.sh']
    for i in files:
        if os.path.exists(i):
            try:
                f = open(i)
                for line in f:
                    line = line.replace('\n','').replace('export ','')
                    line = re.sub(r'^([0-9A-Z\_]+)',r"os.environ['\1']",line)
                    try:
                        exec(line)

                    except Exception, e:
                        print line + " - ERRO: " + str(e)
            except Exception, e:
                print str(e)
                pass

