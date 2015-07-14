# -*- coding: utf-8 -*-

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Spark PEX (Spex)'
copyright = u'2015, Greg Bowyer'
author = u'Greg Bowyer'
version = '0.1.0'
release = '0.1.0'
language = None
exclude_patterns = ['_build']
pygments_style = 'monokai'

# -- Options for HTML output ----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'SparkPEXSpexdoc'

# -- Options for LaTeX output ---------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
}

latex_documents = [
  (master_doc, 'SparkPEXSpex.tex', u'Spark PEX (Spex) Documentation',
   u'Greg Bowyer', 'manual'),
]
