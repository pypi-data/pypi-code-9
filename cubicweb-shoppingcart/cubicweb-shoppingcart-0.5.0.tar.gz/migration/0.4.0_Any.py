add_relation_definition('ShoppingItemType', 'item_available_to', 'CWGroup')
sync_schema_props_perms('item_type')

def get_workflow(cwetype):
    rset = rql('Any W WHERE W workflow_of X, X name %(t)s',
               {'t': cwetype})
    return list(rset.entities())[0]

def get_state(wfeid, sname):
    rset = rql('Any S WHERE S state_of W, W eid %(w)s, S name %(n)s',
               {'w': wfeid, 'n': sname})
    return list(rset.entities())[0]

def get_transition(wfeid, tname):
    rset = rql('Any T WHERE T transition_of W, W eid %(w)s, T name %(n)s',
               {'w': wfeid, 'n': tname})
    return list(rset.entities())[0]

twf = get_workflow('ShoppingCart')
inprogress = get_state(twf.eid, 'in progress')
checkedout = get_state(twf.eid, 'checked out')
checkout = get_transition(twf.eid, 'check out')

paywait = twf.add_state(_('awaiting payment'))
twf.add_transition(_('pay off-line'), (inprogress,), paywait, ('managers',),)
rql('SET S allowed_transition T WHERE S eid %(s)s, T eid %(t)s',
    {'s': paywait.eid, 't': checkout.eid})
commit()
