from fanstatic import Resource, GroupResource
from js.extjs.library import library

js =  Resource(library, 'ext-all.js',
               debug='ext-dev.js')


css = Resource(library, 'resources/css/ext-all.css')

basic = all = GroupResource((js, css,))
