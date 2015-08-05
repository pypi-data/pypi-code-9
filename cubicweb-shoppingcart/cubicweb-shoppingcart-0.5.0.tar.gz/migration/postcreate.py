# postcreate script. You could setup a workflow here for example

def define_shoppingcart_workflow():
    twf = add_workflow(_('shopping cart workflow'), 'ShoppingCart')
    inprogress = twf.add_state(_('in progress'), initial=True)
    paywait = twf.add_state(_('awaiting payment'))
    checkedout = twf.add_state(_('checked out'))
    twf.add_transition(_('pay off-line'), (inprogress,), paywait, ('managers',),)
    twf.add_transition(_('check out'), (inprogress,paywait), checkedout, ('managers',),)

define_shoppingcart_workflow()
