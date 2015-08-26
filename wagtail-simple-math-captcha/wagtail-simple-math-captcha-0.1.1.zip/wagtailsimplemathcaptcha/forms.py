from wagtail.wagtailforms.forms import FormBuilder
from simplemathcaptcha.fields import MathCaptchaField

def create_form_builder(label='', help_text=''):
    class MathCaptchaFormBuilder(FormBuilder):
        def __init__(self, fields):
            super(MathCaptchaFormBuilder, self).__init__(fields)
            # Add mathcaptcha to FIELD_TYPES declaration
            self.FIELD_TYPES.update({'mathcaptcha': self.create_mathcaptcha_field})
    
        def create_mathcaptcha_field(self, field, options):
            return MathCaptchaField(**options)
    
        @property
        def formfields(self):
            # Add mathcaptcha to formfields property
            fields = super(MathCaptchaFormBuilder, self).formfields
            fields['sweetcaptcha'] = MathCaptchaField(label=label, help_text=help_text)
    
            return fields
    
    return MathCaptchaFormBuilder