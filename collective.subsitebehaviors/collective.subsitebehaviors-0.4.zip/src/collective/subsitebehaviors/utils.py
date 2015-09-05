from itertools import chain
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.schema import getFieldsInOrder
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI


def all_dexterity_fieldnames(obj):
   "the schema from FTI plus query IBehaviorAssignable"

   try:
      typename = obj.getPortalTypeName()
      fti = getUtility(IDexterityFTI, name=typename)
   except ComponentLookupError as exc:
      # has no fti, what is this, an ancient Archetype?
      return []
      
   schema = fti.lookupSchema()
   fields = [getFieldsInOrder(schema)]

   behavior_assignable = IBehaviorAssignable(obj)
   if behavior_assignable:
      behaviors = behavior_assignable.enumerateBehaviors()
      for behavior in behaviors:
         fields.append(getFieldsInOrder(behavior.interface))

   return [fn for fn, f in chain(*fields)]