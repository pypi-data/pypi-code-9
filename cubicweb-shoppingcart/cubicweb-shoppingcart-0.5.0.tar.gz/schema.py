from yams.buildobjs import EntityType, String, RelationDefinition, Int

from cubicweb.schema import WorkflowableEntityType, ERQLExpression, RRQLExpression

class ShoppingCart(WorkflowableEntityType):
    __permissions__ = {
        'read':   ('managers', ERQLExpression('X owned_by U'),),
        'add':    ('managers', 'users',),
        'update': ('managers', ERQLExpression('X in_state S, S name "in progress", X owned_by U'),),
        'delete': ('managers',),
        }

class ShoppingItem(EntityType):
    __permissions__ = {
        'read':   ('managers', ERQLExpression('X owned_by U'),),
        'add':    ('managers', 'users',),
        'update': ('managers', ERQLExpression('C items_in_cart X, C in_state S, S name "in progress", C owned_by U'),),
        'delete': ('managers',),
        }
    quantity = Int(required=True)

class ShoppingItemType(EntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    ('managers',),
        'update': ('managers',),
        'delete': ('managers',),
        }
    title = String(maxsize=100, required=True, fulltextindexed=True)
    price = Int(required=True)
    #taxes = Int()

class buyer(RelationDefinition):
    name = 'buyer'
    subject = 'ShoppingCart'
    object = 'CWUser'
    cardinality = '1*'
#     __permissions__ = {
#         'read':   ('managers', RRQLExpression('S owned_by U'),),
#         'add':    ('managers', 'users',),
#         'delete': ('managers', RRQLExpression('S owned_by U'),),
#         }

class items_in_cart(RelationDefinition):
    name = 'items_in_cart'
    subject = 'ShoppingCart'
    object = 'ShoppingItem'
    cardinality = '*1'
    composite = 'subject'
#     __permissions__ = {
#         'read':   ('managers', RRQLExpression('S owned_by U'),),
#         'add':    ('managers', 'users',),
#         'delete': ('managers', RRQLExpression('S owned_by U'),),
#         }

class item_type(RelationDefinition):
    name = 'item_type'
    subject = 'ShoppingItem'
    object = 'ShoppingItemType'
    cardinality = '1*'
    __permissions__ = {
        #'read':   ('managers', RRQLExpression('S owned_by U'),),
        'read':   ('managers', 'users'),
        'add':    ('managers', RRQLExpression('O item_available_to G, U in_group G'),),
        'delete': ('managers', RRQLExpression('S owned_by U'),),
        }

class item_available_to(RelationDefinition):
    name = 'item_available_to'
    subject = 'ShoppingItemType'
    object = 'CWGroup'
    cardinality = '**'
    __permissions__ = {
        'read':   ('managers', 'users'),
        'add':    ('managers',),
        'delete': ('managers',),
        }

