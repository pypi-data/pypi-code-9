"""Form widgets and validators are defined here."""

__all__ = [
    'paste_form',
    'style_select'
]

import tgmochikit
from turbogears import config, validators
from turbogears.widgets import register_static_directory
from tw.api import JSLink, WidgetsList
from tw.forms import ListForm, TableForm, TextArea, TextField, SingleSelectField

from validators import SpamBayesFilter, ValidFormat, ValidStyle


tgmochikit.init(register_static_directory,
    version=config.get('tg_mochikit.version', '1.4'),
    packed=config.get('tg_mochikit.packed', True),
    xhtml=config.get('tg_mochikit.xhtml', False),
    draganddrop=config.get('tg_mochikit.draganddrop', False))
mochikit_js = [JSLink(link='/tg_widgets/tgmochikit/%s' % p)
    for p in tgmochikit.get_paths()]
styleselect_js = JSLink(modname='spammcan',
    filename="static/javascript/styleselect.js")

class PasteFormSchema(validators.Schema):
    title = validators.UnicodeString(max=100, strip=True)
    code = validators.UnicodeString(max=10000, strip=True, not_empty=True)
    format = ValidFormat(if_invalid=None)
    chained_validators = [SpamBayesFilter('code')]

class PasteFormFields(WidgetsList):
    code = TextArea(suppress_label=True, attrs=dict(cols=75, rows=15))
    title = TextField(label_text=_(u'Title:'),
        attrs=dict(maxlength=100, size=50), help_text=_(u'(Optional)'))
    format = SingleSelectField(label_text=_(u'Format:'),
        options=[('text', _(u'No highliting'))])

class StyleSelectForm(ListForm):
    class fields(WidgetsList):
        st = SingleSelectField(label_text=_(u'Color scheme:'),
            options=[('default', _(u'Default'))])
    submit_text = _(u'Go')
    javascript = mochikit_js + [styleselect_js]

style_select = StyleSelectForm('styleselect')

paste_form = TableForm(
    fields = PasteFormFields(),
    validator = PasteFormSchema()
)
