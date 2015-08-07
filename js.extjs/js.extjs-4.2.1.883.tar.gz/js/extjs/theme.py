from fanstatic import Resource
from js.extjs.library import library
from js.extjs import extjs

defaultThemes = ('gray', 'access', 'neptune',)
themes = {}


def add_theme(themeName):
    css = Resource(library, 'resources/css/ext-all-%s.css' % themeName,
                   depends=[])
    js  = Resource(library, 'ext-theme-%s.js' % themeName, depends=[css])

    global themes
    themes[themeName] = globals()[themeName] = js
    return js

for themeName in defaultThemes:
    add_theme(themeName)
