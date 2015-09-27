from django.utils.safestring import mark_safe as S
from django.template.loader import get_template
from django.template import Context


def messageBox(messages):
    return S(get_template('messages/messageBox.html').render(Context({'messages':messages})))
