"""template-specific forms/views/actions/components"""

from logilab.common.decorators import monkeypatch
from logilab.mtconverter import xml_escape

from rql.utils import decompose_b26

from cubicweb.predicates import is_instance
from cubicweb.web import formfields as ff, formwidgets as fw
from cubicweb.web.views import (basecontrollers, formrenderers, forms,
                                autoform, primary, uicfg)
from cubicweb.view import EntityView


def subject_buyer_vocabulary(form, field):
    if form._cw.user.matching_groups('managers'):
        rset = form._cw.execute('Any U WHERE U is CWUser')
    else:
        rset = form._cw.execute('Any U WHERE U is CWUser, U eid %(x)s', {'x': form._cw.user.eid})
    if rset:
        return [(entity.dc_long_title(), entity.eid) for entity in rset.entities()
                if entity.eid != form.edited_entity.eid]
    return []

uicfg.primaryview_section.tag_subject_of(('ShoppingCart', 'items_in_cart', '*'), 'relations')
uicfg.primaryview_display_ctrl.tag_subject_of(('ShoppingCart', 'items_in_cart', '*'), {'order':30})

uicfg.autoform_field_kwargs.tag_subject_of(('ShoppingCart', 'buyer', 'CWUser'),
                                           {'choices': subject_buyer_vocabulary})
uicfg.autoform_field_kwargs.tag_subject_of(('ShoppingCart', 'items_in_cart', 'ShoppingItem'),
                                           {'order': 30})

class ShoppingCartPrimaryView(primary.PrimaryView):

    __select__ = primary.PrimaryView.__select__ & is_instance('ShoppingCart')

    def render_entity_attributes(self, entity):
        return

    def render_entity_relations(self, entity):
        _ = self._cw._
        if not entity.items_in_cart:
            self.w(u'<h4>%s</h4>' % _(u'this cart is empty'))
            return
        self._cw.add_css('cubicweb.acl.css')
        self.w(u'<table class="listing">')
        self.w(u'<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' %
               (_('item'), _('quantity'), _('unit price'), _('total price')))
        total = 0
        for item in entity.items_in_cart:
            subtotal = item.quantity * item.item.price
            self.w(u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                   (xml_escape(item.item.title), item.quantity, item.item.price, subtotal))
            total += subtotal
        self.w(u'<tr><th colspan="3">%s</th><th>%s</th></tr>' % (_('total'), total))
        self.w(u'</table>')

class ShoppingCartEntityFormRenderer(formrenderers.EntityFormRenderer):
    __select__ = is_instance('ShoppingCart')

    main_form_title = None

    explanation_text = u''

    def open_form(self, form, values):
        if self.explanation_text:
            para = u'<p>%s</p>' % self._cw._(self.explanation_text)
        else:
            para = u''
        return para + super(ShoppingCartEntityFormRenderer, self).open_form(form, values)

class ShoppingItemWidget(fw.FieldWidget):

    def render(self, form, field, renderer):
        form._cw.add_js('cubes.shoppingcart.js')
        entity = form.edited_entity
        result = []
        w = result.append
        if entity.has_eid():
            for item in entity.items_in_cart:
                w(_item_inline_form(item, entity.eid))
                w('<br/>')
        w(u"""<div id="cartitems">
<div id="cartitemstable"></div>
<a id="additemincart" href="javascript: addItemInCart('%s')">%s</a>
</div>""" % (entity.eid, form._cw._('add item to cart')))
        return u'\n'.join(result)

uicfg.autoform_section.tag_subject_of(('ShoppingCart', 'items_in_cart', 'ShoppingItem'), 'main', 'attributes')
uicfg.autoform_field_kwargs.tag_subject_of(('ShoppingCart', 'items_in_cart', 'ShoppingItem'),
                                           {'widget': ShoppingItemWidget})

try:
    class ShoppingItemInlineForm(forms.EntityFieldsForm):
        __regid__ = 'inline-shoppingitem-form'
        form_renderer_id = 'inline-shoppingitem-renderer'
        quantity = autoform.etype_relation_field('ShoppingItem', 'quantity')
        item_type = autoform.etype_relation_field('ShoppingItem', 'item_type')
except KeyError:
    import warnings
    warnings.warn('KeyError raised when defining class ShoppingItemInlineForm, '
                  'if this does not happen during a migration that will add '
                  'the shoppingcart cube, you have a problem')

class ShoppingItemFormRenderer(formrenderers.FormRenderer):
    __regid__ = 'inline-shoppingitem-renderer'

    def render(self, form, values):
        data = []
        w = data.append
        w(u'<div id="cartitem%s">' % form.edited_entity.eid)
        self.render_fields(w, form, values)
        w('''<span>[<a href="javascript: removeItemFromCart('%s')">%s</a>]</span>
</div>''' % (form.edited_entity.eid, self._cw._('remove item from cart')))
        return '\n'.join(data)

    def _render_fields(self, fields, w, form):
        for field in fields:
            w(u'<span>%s</span> ' % field.render(form, self))


def _item_inline_form(item, carteid):
    form = item._cw.vreg['forms'].select('inline-shoppingitem-form',
                                         item._cw, entity=item, mainform=False)
    form.add_hidden('items_in_cart-subject:%s' % carteid, value=item.eid)
    return form.render()


@monkeypatch(basecontrollers.JSonController)
@basecontrollers.xhtmlize
def js_add_item_in_cart(self, item_eid, cart_eid):
    item = self._cw.vreg['etypes'].etype_class('ShoppingItem')(self._cw)
    item.eid = decompose_b26(item_eid)
    return _item_inline_form(item, cart_eid)
