twf = rql('Any W WHERE W is Workflow, W workflow_of X, X name "ShoppingCart"', ask_confirm=False).get_entity(0,0)
for transition in twf.reverse_transition_of:
    if transition.name == 'check out':
        transition.set_permissions(('managers',), reset=True)
commit()
