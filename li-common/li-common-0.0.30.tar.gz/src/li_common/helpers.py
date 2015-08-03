# -*- coding: utf-8 -*-

"""
Funções para auxiliarem no desenvolvimento
"""

import time

from unicodedata import normalize
from functools import wraps

from repositories.plataforma.models import Conta, Usuario, Contrato

from conexoes.email import TemplateEmailSender

import logging
logger = logging.getLogger("helpers")


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
                    if logger:
                        logger.warning(msg)
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
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])


def send_email(template_file=None, context=None, contrato_id=None, conta_id=None, usuario_id=None, salva_evidencia=True, to_email=None):
    contexto_evidencia = {}
    contexto_evidencia.update(context)
    if conta_id is not None:
        try:
            conta = Conta.objects.get(id=conta_id)
            context['conta'] = conta
        except Conta.DoesNotExist:
            logger.error("Não foi encontrada Conta com id={}".format(conta_id))
            return False

        if context['conta'].contrato_id is not None and contrato_id is None:
            contrato_id = context['conta'].contrato_id

    usuarios = None
    if to_email is None:
        if conta_id is not None or usuario_id is not None:
            kwargs = {}
            if conta_id is not None:
                kwargs['conta_id'] = conta_id

            if usuario_id is not None:
                kwargs['id'] = usuario_id

            usuarios = Usuario.objects.filter(**kwargs)
            logger.debug(usuarios.query)

    # TODO: fazer um if para pegar o contrato_id do primeiro usuario caso nao tenha contrato_id definido
    if contrato_id is not None or usuarios is not None:
        try:
            contrato = Contrato.objects.get(id=contrato_id)
            context['contrato'] = contrato
        except Contrato.DoesNotExist:
            logger.error("Não foi encontrado Contrato com id={}".format(contrato_id))
            return False

    from_email = 'nao-responder@' + context['contrato'].dominio
    if to_email is not None:
        if usuario_id is not None:
            try:
                context["usuario"] = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                pass
        TemplateEmailSender(template_file, context, from_email, to_email, salva_evidencia, contexto_evidencia, contrato_id, conta_id, usuario_id).send_async()
    else:
        for item in usuarios:
            context['usuario'] = item
            to_email = item.email
            TemplateEmailSender(template_file, context, from_email, to_email, salva_evidencia, contexto_evidencia, contrato_id, conta_id, usuario_id).send_async()