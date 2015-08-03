from bst.pygasus.core import ext
from bst.pygasus.demo import schema


class Card(ext.Model):
    ext.schema(schema.ICard)
    id = 0
    type = ''
    text = ''
    costs = 0
    colors = ''
    layout = ''
    name = ''
    power = ''
    toughness = ''
    availability = 0
