from ftw.jsondump.dexterity.base import PlainFieldExtractor
from plone.app.textfield.value import RichTextValue


class RichTextExtractor(PlainFieldExtractor):

    def extract(self, name, data, config):
        storage = self.field.interface(self.context)
        value = getattr(storage, name)
        if isinstance(value, RichTextValue):
            data.update({self.key: value.raw,
                         self.key + ':mimeType': value.mimeType,
                         self.key + ':outputMimeType': value.outputMimeType,
                         self.key + ':encoding': value.encoding})
        else:
            data[self.key] = value
