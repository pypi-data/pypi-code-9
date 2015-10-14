from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _

from changer.c5.shoppingcart import (SessionCart, REDIRECT_TO,
                                     FAIL, REDIRECT_AFTER_CHECKOUT,
                                     SUCCESS_MSG)
from changer.c5.shoppingcart.models import Item
from changer.c5.shoppingcart.forms import AnonymousRegistrationForm
#from changer.c5.shoppingcart import cart_checkout_signal


def cart_add(request,
        class_name='Product',
        qty_field='quantity',
        price_field='price',
        product_field='product',
        redirect_to=REDIRECT_TO):
    """
    Default assumes cart items are relations of a 'Product' class,
    alternatively, the `klass` argument can be passed to the function
    via a custom url
    """

    session_cart = SessionCart(request)

    if isinstance(class_name, (str, unicode)):
        assert False, _(u"Class cannot be a string. Did you define a custom "
                         "url and pass it your Product class?")
    elif isinstance(class_name, object):
        klass = class_name
    else:
        raise Item.ProductClassUndefined

    if request.method == 'POST':
        product_key = request.POST.get(product_field)
        try:
            product = klass._default_manager.get(id=product_key)
        except klass.DoesNotExist:
            messages.add_message(request, messages.WARNING, FAIL)
        else:
            session_cart.add(request, product, getattr(product, price_field), request.POST.get(qty_field))
        finally:
            return HttpResponseRedirect(reverse('cart-view'))
    return HttpResponseRedirect(redirect_to)


def cart_view(request, template_name='shoppingcart/cart-overview.html'):
    """
    Display the cart.
    """
    session_cart = SessionCart(request)
    extra_context = {
        'items': session_cart.cart.items.all(),
    }

    return render_to_response(template_name, extra_context, RequestContext(request))


def cart_increase(request, item_id):
    """
    Adds one item to a product in the cart
    """
    session_cart = SessionCart(request)
    item = get_object_or_404(Item, pk=item_id)
    item.increase()
    return HttpResponseRedirect(reverse('cart-view'))


def cart_decrease(request, item_id):
    """
    Removes one item from a product in the cart
    """
    session_cart = SessionCart(request)
    item = get_object_or_404(Item, pk=item_id)
    item.decrease()
    return HttpResponseRedirect(reverse('cart-view'))


def cart_remove(request, item_id):
    """
    Removes a product from the cart
    """
    session_cart = SessionCart(request)
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('cart-view'))


def cart_checkout(request):
    """
    Does cart checkout. Sends cart info to whoever needs it via a signal.
    Then clears the cart out of the session.
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("get-customer-info"))
    else:
        session_cart = SessionCart(request)
        send_invoice_email(request, session_cart,
            {'first_name': request.user.first_name,
             'last_name':  request.user.last_name,
             'email':      request.user.email})
    
    #cart_checkout_signal.send(sender=session_cart,
    #                          request=request)
    session_cart.clear()
    return HttpResponseRedirect(reverse(REDIRECT_AFTER_CHECKOUT))


def cart_get_customer_info(request, cart=None, form_class=AnonymousRegistrationForm,
                    template="shoppingcart/cart-registration.html"):
    if request.method == 'POST':
        session_cart = SessionCart(request)
        form = form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            send_invoice_email(request, session_cart,
                {'first_name': cleaned_data['first_name'],
                 'last_name':  cleaned_data['last_name'],
                 'email':      cleaned_data['email']})
            session_cart.clear()
            return HttpResponseRedirect(reverse(REDIRECT_AFTER_CHECKOUT))
    else:
        form = form_class()
    return render_to_response(template, {'form': form}, RequestContext(request))


# @receiver(cart_checkout_signal)
# def checkout_handler(sender, request, **kwargs):
#    """
#    Signal receiver for cart checkout. Puts the cart in the 
#    session for an additional check after the cart redirects.
#    """
#    #assert False, sender.cart
#    request.session['anonymous_cart'] = sender.cart.cart_id
#    #assert False, sender.cart.items.all()


def send_invoice_email(request, session_cart, context={}):
    """
    Send invoice email on checkout
    """
    context.update({'items': session_cart.cart.items.all()})

    subject = loader.render_to_string('email/invoice_subject.txt', {})
    message = loader.render_to_string('email/invoice_body.txt', context)

    from django.core import mail
    mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.INVOICE_RECIPIENTS)
    
    messages.add_message(request, messages.SUCCESS, SUCCESS_MSG)

