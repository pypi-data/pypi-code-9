
import sys, os

print "PATH", os.path.abspath("..")
sys.path.insert(0, os.path.abspath(".."))

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

project = u'show'
copyright = u'2015, Jonathan Eunice'

version = '1.2'
release = '1.2.4'

exclude_patterns = ['_build']


pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'

#html_logo = None
#html_favicon = None

html_static_path = ['_static']


html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

html_use_opensearch = 'http://show.readthedocs.org'

# Output file base name for HTML help builder.
htmlhelp_basename = 'showdoc'
