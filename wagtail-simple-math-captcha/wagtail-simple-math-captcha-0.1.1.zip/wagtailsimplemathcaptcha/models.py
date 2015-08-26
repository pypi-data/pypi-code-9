from six import text_type

from simplemathcaptcha.fields import MathCaptchaField

from wagtail.wagtailadmin.utils import send_mail
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractForm

from .forms import create_form_builder

class CaptchaLabelMixin(object):
    captcha_label = ''
    captcha_help_text = ''

    def get_captcha_label(self):
        return self.captcha_label
    
    def get_captcha_help_text(self):
        return self.captcha_help_text

class MathCaptchaEmailForm(AbstractEmailForm, CaptchaLabelMixin):
    """A MathCaptchaForm Page. Pages implementing a captcha form with email notification should inhert from it"""

    is_abstract = True  # Don't display me in "Add"

    def __init__(self, *args, **kwargs):
        super(MathCaptchaEmailForm, self).__init__(*args, **kwargs)
        self.form_builder = create_form_builder(label=self.get_captcha_label(), help_text=self.get_captcha_help_text())

    def process_form_submission(self, form):
        super(AbstractEmailForm, self).process_form_submission(form)

        if self.to_address:
            content = ''
            for x in form.fields.items():
                if not isinstance(x[1], MathCaptchaField):  # exclude MathCaptchaField from notification
                    content += '\n' + x[1].label + ': ' + text_type(form.data.get(x[0]))
            send_mail(self.subject, content, [self.to_address], self.from_address,)

    class Meta:
        abstract = True


class MathCaptchaForm(AbstractForm, CaptchaLabelMixin):
    """A SweetCaptchaForm Page. Pages implementing a captcha form should inhert from it"""

    is_abstract = True  # Don't display me in "Add"

    def __init__(self, *args, **kwargs):
        super(MathCaptchaForm, self).__init__(*args, **kwargs)
        self.form_builder = create_form_builder(label=self.get_captcha_label(), help_text=self.get_captcha_help_text())

    class Meta:
        abstract = True
