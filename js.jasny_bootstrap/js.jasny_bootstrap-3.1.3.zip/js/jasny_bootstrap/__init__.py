from fanstatic import Library, Resource, Group
from js.jquery import jquery

library = Library('jasny_bootstrap', 'resources')

# Define the resources in the library like this.
# For options and examples, see the fanstatic documentation.
# resource1 = Resource(library, 'style.css')

jasny_bootstrap_css = Resource(
    library,
    'css/jasny-bootstrap.css'
)

jasny_bootstrap_js = Resource(
    library, 'js/jasny-bootstrap.js',
    depends=[jquery],
    minified='js/jasny-bootstrap.min.js'
)

jasny_bootstrap = Group(
    [jasny_bootstrap_css, jasny_bootstrap_js])
