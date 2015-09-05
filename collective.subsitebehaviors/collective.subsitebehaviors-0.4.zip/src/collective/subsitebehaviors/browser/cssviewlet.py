import re
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.root import getNavigationRoot
#from ftw.subsite.interfaces import ISubsite
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..behaviors import ISubSite
from ..utils import all_dexterity_fieldnames

decamel_regxp = re.compile('(.)([A-Z][a-z]+)')


class CSSViewlet(ViewletBase):

   template = ViewPageTemplateFile('cssviewlet.pt')

   def __init__(self, context, request, view, manager=None):
      super(CSSViewlet, self).__init__(context, request, view, manager)
      self.subsite = None

   def render(self):
      nav_root = api.portal.get_navigation_root(context=self.context)
      if ISubSite.providedBy(nav_root):
         self.subsite = nav_root
         return self.template()
      else:
         self.subsite = None
         return ''


   def parse_fieldname(self, name):
      "parse css_tag[tagname]_id[id]_class[classname]_attr[attrname] format"
      parsethese = ("tag", "id", "class", "cssattr")
      rawspecs = name.split('_')
      parsed_spec = [None, None, None, None]
      for rawspec in rawspecs:
         for idx, parsed in enumerate(parsethese):
            value = rawspec[len(parsed):] if parsed in rawspec else None
            if value:
               parsed_spec[idx] = value
      return parsed_spec

 
   def get_css(self):
      "generate css from specially formatted fields"
      
      if not self.subsite:
         return ''
         
      css_fields = [n for n in all_dexterity_fieldnames(self.subsite) if n.startswith("css_")]
      styles = []
      
      for css_fn in css_fields:
         tag, id, klass, cssattr = self.parse_fieldname(css_fn[4:]) # strip prefix
         selector = tag
         selector += '#' + id if id else ''
         selector += '.' + klass if klass else ''
         
         # convert BackgroundColor to background-color
         cssattr =  decamel_regxp.sub(r'\1-\2', cssattr) if cssattr else ''

         # if cssatr, field value has just css attr value, othewise full 'attr: val' css"
         field_value = getattr(self.context, css_fn)
         if not field_value:
            field_value = ''
         attr_plus_val = cssattr + ": " + field_value if cssattr else field_value
         
         style = selector + " {\n  %s;\n}" % attr_plus_val         
         styles.append(style)

      return '\n'.join(styles)
      
      
      