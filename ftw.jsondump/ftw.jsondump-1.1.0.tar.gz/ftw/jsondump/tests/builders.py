from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder
from plone.namedfile.file import NamedBlobFile


class DXItemBuilder(DexterityBuilder):
    portal_type = 'DXItem'

    def attach_image(self, image_asset):
        image = NamedBlobFile(data=image_asset.bytes(),
                              filename=unicode(image_asset.name))
        return self.having(image_field=image)

    def attach_file(self, file_asset):
        file_ = NamedBlobFile(data=file_asset.bytes(),
                              filename=unicode(file_asset.name))
        return self.having(file_field=file_)


builder_registry.register('dx item', DXItemBuilder)
