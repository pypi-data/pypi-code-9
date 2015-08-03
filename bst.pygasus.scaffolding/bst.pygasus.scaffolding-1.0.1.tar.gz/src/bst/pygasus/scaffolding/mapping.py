from bst.pygasus.core import ext


class ModelClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.model'
    path = 'scaffolding/model'


class StoreClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.store'
    path = 'scaffolding/store'


class BufferedStoreClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.bufferedstore'
    path = 'scaffolding/bufferedstore'


class FormClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.form'
    path = 'scaffolding/form'


class DisplayClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.display'
    path = 'scaffolding/display'


class GridClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.grid'
    path = 'scaffolding/grid'


class GridEditClassPathMapping(ext.ClassPathMapping):
    namespace = 'scaffolding.editgrid'
    path = 'scaffolding/editgrid'
