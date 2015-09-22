from fanstatic import Library, Resource, Group
from js.jquery import jquery

library = Library('jquery_datatables', 'resources')

# Define the resources in the library like this.
# For options and examples, see the fanstatic documentation.
# resource1 = Resource(library, 'style.css')

jquery_datatables_css = Resource(
    library,
    'media/css/jquery.dataTables.css'
)

jquery_datatables_js = Resource(
    library, 'media/js/jquery.dataTables.js',
    depends=[jquery],
    minified='media/js/jquery.dataTables.min.js'
)

jquery_datatables = Group(depends=[
        jquery_datatables_css, jquery_datatables_js]
)

autofill_css = Resource(
    library, 'extensions/AutoFill/css/dataTables.autoFill.css')

autofill = Resource(
    library, 'extensions/AutoFill/js/dataTables.autoFill.js',
    depends=[jquery_datatables_js, autofill_css],
    minified='extensions/AutoFill/js/dataTables.autoFill.min.js')

colreorder_css = Resource(
    library, 'extensions/ColReorder/css/dataTables.colReorder.css')

colreorder = Resource(
    library, 'extensions/ColReorder/js/dataTables.colReorder.js',
    depends=[jquery_datatables_js, colreorder_css],
    minified='extensions/ColReorder/js/dataTables.colReorder.min.js')

colvis_css = Resource(
    library, 'extensions/ColVis/css/dataTables.colVis.css')

colvis_jqueryui_css = Resource(
    library, 'extensions/ColVis/css/dataTables.colvis.jqueryui.css')

colvis = Resource(
    library, 'extensions/ColVis/js/dataTables.colVis.js',
    depends=[jquery_datatables_js, colvis_css],
    minified='extensions/ColVis/js/dataTables.colVis.min.js')

fixed_columns = Resource(
    library, 'extensions/FixedColumns/js/dataTables.fixedColumns.js',
    depends=[jquery_datatables_js],
    minified='extensions/FixedColumns/js/dataTables.fixedColumns.min.js')

fixed_header = Resource(
    library, 'extensions/FixedHeader/js/dataTables.fixedHeader.js',
    depends=[jquery_datatables_js],
    minified='extensions/FixedHeader/js/dataTables.fixedHeader.min.js')

keytable_css = Resource(
    library, 'extensions/KeyTable/css/dataTables.keyTable.css')

keytable = Resource(
    library, 'extensions/KeyTable/js/dataTables.keyTable.js',
    depends=[jquery_datatables_js, keytable_css],
    minified='extensions/KeyTable/js/dataTables.keyTable.min.js')

responsive_css = Resource(
    library, 'extensions/Responsive/css/dataTables.responsive.css')

responsive = Resource(
    library, 'extensions/Responsive/js/dataTables.responsive.js',
    depends=[jquery_datatables_js, responsive_css],
    minified='extensions/Responsive/js/dataTables.responsive.min.js')

scroller_css = Resource(
    library, 'extensions/Scroller/css/dataTables.scroller.css')

scroller = Resource(
    library, 'extensions/Scroller/js/dataTables.scroller.js',
    depends=[jquery_datatables_js, scroller_css],
    minified='extensions/Scroller/js/dataTables.scroller.min.js')

table_tools_css = Resource(
    library, 'extensions/TableTools/css/dataTables.tableTools.css')

table_tools_js = Resource(
    library, 'extensions/TableTools/js/dataTables.tableTools.js',
    minified='extensions/TableTools/js/dataTables.tableTools.min.js',
    depends=[jquery_datatables_js, table_tools_css])

table_tools = Group(depends=[table_tools_js, table_tools_css])
