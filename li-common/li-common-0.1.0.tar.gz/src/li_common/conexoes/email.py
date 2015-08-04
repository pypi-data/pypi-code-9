from ..conexoes.worker import WorkerConnect

from django.template.loader import get_template
from django.template import Context

import re
from copy import copy


# SEMPRE que usar esta funcao, os templates devem estar na maquina.
# Atualmente baixado com LI-Standalone/scripts/atualizar_email_templates.sh
# unattis
class TemplateEmailSender(object):
    def __init__(self, template_file, context, from_email, to_email, salva_evidencia, context_template, contrato_id, conta_id, usuario_id):
        template = get_template(template_file + ".html")
        self.html_message = template.render(Context(context))
        self.subject = self.extrai_assunto_do_titulo_do_html()
        self.from_email = from_email
        if not type(to_email) is list:
            to_email = [to_email]
        self.to_email = to_email
        self.salva_evidencia = salva_evidencia
        self.evidencia = {
            'template': template_file,
            'context': copy(context_template),
            'contrato_id': contrato_id,
            'conta_id': conta_id,
            'usuario_id': usuario_id,
            'subject': self.subject,
            'from_email': self.from_email,
            'to_email': self.to_email,
            'html_message': self.html_message
        }

    def salvando_envidencia_de_envio_de_email(self):
        args = {"tipo_evidencia": 'utils.send_email_template', "evidencia": self.evidencia}
        WorkerConnect().execute('async.utils.salvar_evidencia', args=args)

    def extrai_assunto_do_titulo_do_html(self):
        match = re.findall(r'<title>(.*)</title>', self.html_message)
        subject = match[0]
        return subject

    def send_async(self):
        args = {"subject": self.subject, "from_email": self.from_email, "to_email": self.to_email, "html_message": self.html_message, "text_message": ""}
        WorkerConnect().execute('async.utils.send_email', args=args)
        if self.salva_evidencia:
            self.salvando_envidencia_de_envio_de_email()