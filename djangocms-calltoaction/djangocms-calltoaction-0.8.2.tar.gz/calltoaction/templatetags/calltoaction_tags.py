from django import template

from classytags.core import Options
from classytags.helpers import AsTag
from classytags.arguments import Argument

from ..models import CallToActionRepository


class GetCallToAction(AsTag):
    name = 'get_call_to_action'

    options = Options(
        Argument('code', required=True),
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def get_value(self, context, code):
        try:
            return CallToActionRepository.objects.get(code=code).rendered()
        except CallToActionRepository.DoesNotExist:
            return ''


register = template.Library()
register.tag(GetCallToAction)
