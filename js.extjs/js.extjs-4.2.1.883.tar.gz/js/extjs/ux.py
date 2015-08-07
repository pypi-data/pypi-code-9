from js.extjs import extjs
from js.extjs.library import library
from fanstatic import Resource, GroupResource, UnknownResourceError


ux_names = [
    'BoxReorderer',
    'CellDragDrop',
    'DataTip',
    'DataViewTransition',
    'FieldReplicator',
    'GMapPanel',
    'GroupTabPanel',
    'GroupTabRenderer',
    'IFrame',
    'LiveSearchGridPanel',
    'PreviewPlugin',
    'ProgressBarPager',
    'RowExpander',
    'SlidingPager',
    'Spotlight',
    'TabCloseMenu',
    'TabReorderer',
    'TabScrollerMenu',
    'ToolbarDroppable',
    'TreePicker'
]

ux = {}

def add_ux(ux_name):
    depends=[extjs.js]
    try:
        css = Resource(library, 'examples/css/%s.css' % ux_name,
                      depends=[])
        depends=[css, extjs.js]
    except UnknownResourceError:
        pass
    js = Resource(library, 'examples/ux/%s.js' % ux_name,
                  depends=depends)

    global ux
    ux[ux_name] = globals()[ux_name] = js
    return js

for name in ux_names:
    add_ux(name)

all = basic_with_ux = GroupResource(ux.values())