# -*- coding: utf-8 -*-
from tw2.recaptcha import ReCaptchaWidget as BadReCaptchaWidget
from tw2.recaptcha.validator import ReCaptchaValidator as BadReCaptchaValidator
__author__ = 'vahid'

class ReCaptchaWidget(BadReCaptchaWidget):
    """
    Hack by Vahid Mardani, due the tw2.recaptcha validation bug
    """
    _sub_compound = True
    pass

class ReCaptchaValidator(BadReCaptchaValidator):
    """
    Hack by Vahid Mardani, due the tw2.recaptcha validation bug
    """
    not_empty = True