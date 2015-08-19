from bst.pygasus.core import ext

from js.extjs.theme import themes

from fanstatic import Library
from fanstatic import Resource


library = Library('demo', 'app')
styles = Resource(library, 'resources/css/styles.css')
favicon = Resource(library, 'resources/images/biel.ico')


class DemoContext(ext.ApplicationContext):

    title = 'Demo'
    application = 'bst.pygasus.demo.Application'
    namespace = 'bst.pygasus.demo'
    resources = Resource(library, 'application.js',
                         depends=[ext.extjs_resources_skinless,
                                  themes['neptune'],
                                  styles,
                                  favicon])


class ViewClassPathMapping(ext.ClassPathMapping):
    namespace = 'bst.pygasus.demo.view'
    path = 'fanstatic/demo/view'


class ControllerClassPathMapping(ext.ClassPathMapping):
    namespace = 'bst.pygasus.demo.controller'
    path = 'fanstatic/demo/controller'
