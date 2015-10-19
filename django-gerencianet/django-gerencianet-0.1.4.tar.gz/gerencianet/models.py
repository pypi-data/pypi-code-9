from jsonfield import JSONField
from django.db.models.base import Model
from django.db.models.fields import DateTimeField, TextField, EmailField, IntegerField
from gerencianet.constants import GatewayStatusResponse


class PaymentLog(Model):
    STATUS_CHOICES = (
        (GatewayStatusResponse.success, "Success"),
        (GatewayStatusResponse.error, "Error"),
    )

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    timestamp = DateTimeField(auto_now=True)
    data = TextField()
    status = IntegerField(default=GatewayStatusResponse.success, choices=STATUS_CHOICES)
    identifier = TextField(null=True, blank=True)
    email = EmailField(null=True)
    response = JSONField(null=True)

    def __unicode__(self):
        return str(self.timestamp) + '-' + str(self.data) + '-' + str(self.email) + '-' + str(self.status)
