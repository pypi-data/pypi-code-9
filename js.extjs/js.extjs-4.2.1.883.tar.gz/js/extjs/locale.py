from fanstatic import Resource
from js.extjs.library import library

locale_names = (
    'ext-lang-af',
    'ext-lang-bg',
    'ext-lang-ca',
    'ext-lang-cs',
    'ext-lang-da',
    'ext-lang-de',
    'ext-lang-el_GR',
    'ext-lang-en_AU',
    'ext-lang-en_GB',
    'ext-lang-en',
    'ext-lang-es',
    'ext-lang-et',
    'ext-lang-fa',
    'ext-lang-fi',
    'ext-lang-fr_CA',
    'ext-lang-fr',
    'ext-lang-gr',
    'ext-lang-he',
    'ext-lang-hr',
    'ext-lang-hu',
    'ext-lang-id',
    'ext-lang-it',
    'ext-lang-ja',
    'ext-lang-ko',
    'ext-lang-lt',
    'ext-lang-lv',
    'ext-lang-mk',
    'ext-lang-nl',
    'ext-lang-no_NB',
    'ext-lang-no_NN',
    'ext-lang-pl',
    'ext-lang-pt_BR',
    'ext-lang-pt_PT',
    'ext-lang-pt',
    'ext-lang-ro',
    'ext-lang-ru',
    'ext-lang-sk',
    'ext-lang-sl',
    'ext-lang-sr_RS',
    'ext-lang-sr',
    'ext-lang-sv_SE',
    'ext-lang-th',
    'ext-lang-tr',
    'ext-lang-ukr',
    'ext-lang-vn',
    'ext-lang-zh_CN',
    'ext-lang-zh_TW',
)


locale = {}


def add_locale(local_name):
    js = Resource(library, 'locale/%s.js' % local_name,
                   depends=[])

    global locale
    path_name = local_name.replace('-', '_')
    locale[path_name] = globals()[path_name] = js
    return js

for name in locale_names:
    add_locale(name)
