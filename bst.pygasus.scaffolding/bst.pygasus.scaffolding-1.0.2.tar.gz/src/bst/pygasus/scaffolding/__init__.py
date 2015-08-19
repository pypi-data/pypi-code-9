import os
from genshi.template import TemplateLoader
loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates'))
