from ftw.jsondump.interfaces import IPartial
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class PropertiesPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        data = {'_properties': []}

        for property_id in self.context.propertyIds():
            property_value = self.context.getProperty(property_id)
            property_type = self.context.getPropertyType(property_id)

            if property_type == 'date':
                property_value = str(property_value)
            elif property_type == 'long':
                property_value = int(property_value)
            elif property_type == 'lines':
                property_value = list(property_value)

            data['_properties'].append([property_id,
                                        property_value,
                                        property_type])

        return data
