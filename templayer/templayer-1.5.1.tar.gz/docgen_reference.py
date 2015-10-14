#!/usr/bin/python

"""
Reference documentation generator for Templayer

  http://excess.org/templayer/

library to build dynamic html that provides clean separation of form
(html+css+javascript etc..) and function (python code) as well as
making cross-site scripting attacks and improperly generated html
very difficult.

Copyright (c) 2003-2009 Ian Ward

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software 
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 
02110-1301, USA.
"""

import pydoc
import types

import templayer

html_template = """<html>
<head>
<title>Templayer %version% Reference</title>
<style type="text/css">
	h1 { text-align: center; }
	h2 { margin: 40px 0 0 0; padding: 10px;  background: #6d96e8;}
	h3 { margin: 0 0 3px 0; padding: 12px 6px 6px 6px; background: #efef96;}
	.l1 { margin: 12px 0 0 0; }
	.l2 { margin-left: 20px; }
</style>
<body>
<a name="top"></a>
<h1>Templayer %version% Reference</h1>

<div style="text-align: center;">
<a href="http://excess.org/templayer/">Templayer Home Page</a> /
<a href="tutorial.html">Tutorial</a> /
Reference
</div>
<br>
%toc%
<br>
%contents%
</body>
</html>"""


class TemplayerHTMLDoc( pydoc.HTMLDoc ):
	def heading(self, title, fgcol, bgcol, extras=''):
		return extras

	def section(self, title, fgcol, bgcol, contents, width=6,
	                prelude='', marginalia=None, gap='&nbsp;'):
		if " = " in title:
			visible, tail = title.split(" = ",1)
			aname = tail.split('">',1)[0]
			aname = aname.split('"',1)[1]
			aname = aname.replace(" ","_")
			title = '<a name="'+aname+'"></a>'+visible
		return '<h3>%s <span style="font-size:small; padding-left: 20px">[<a href="#top">back to top</a>]</span></h3>%s' % (title,contents)
		
	def namelink(self, name, *ignore):
		return name
	
	def classlink(self, obj, modname):
		return obj.__name__
	
	def modulelink(self, obj):
		return obj.__name__
	
	def modpkglink(self, (name, path, ispackage, shadowed) ):
		return name
	
	def markup(self, text, escape=None, funcs={}, classes={}, methods={}):
		return pydoc.HTMLDoc.markup( self, text, escape )


def main():
	html = TemplayerHTMLDoc()
	contents = []
	doc = []
	
	contents.append('<table width="100%"><tr><td width="50%" valign="top">')
	
	for obj, name in [
		(None,"Template classes"),
		(templayer.Template,"Template"),
		(templayer.HTMLTemplate,"HTMLTemplate"),
		(None,"Output classes"),
		(templayer.FileWriter,"FileWriter"),
		(templayer.Layer,"Layer"),
		(None,"Django integration"),
		(templayer.django_form,"django_form"),
		(templayer.django_template_loader,"django_template_loader"),
		(templayer.django_template,"django_template"),
		(templayer.django_view,"django_view"),
		(templayer.get_django_template,"get_django_template"),
		(None,"Utility functions"),
		(templayer.html_url_encode,"html_url_encode"),
		(templayer.html_href,"html_href"),
		(templayer.html_target,"html_target"),
		(templayer.html_escape,"html_escape"),
		(None,None),
		(None,"HTML Markup (yes, markup language markup)"),
		(templayer.join,"join"),
		(templayer.pluralize,"pluralize"),
		(templayer.urljoin,"urljoin"),
		(templayer.href,"href"),
		(templayer.target,"target"),
		(templayer.BR,"BR"),
		(templayer.P,"P"),
		(templayer.I,"I"),
		(templayer.B,"B"),
		(templayer.U,"U"),
		(templayer.entity,"entity"),
		(templayer.expand_html_markup,"expand_html_markup"),
		(templayer.RawHTML,"RawHTML"),
		]:
		if name is None:
			contents.append('</td><td width="50%" valign="top">')
		elif obj is None:
			contents.append('<div class="l1">%s</div>' % name)
			doc.append('<h2>%s</h2>' % name )
		else:
			lname = name
			if type(obj) != types.ClassType: #dirty hack
				doc.append('<a name="%s"></a><h3>function %s <span style="font-size:small; padding-left: 20px">[<a href="#top">back to top</a>]</span></h3>' % (name,name) )
			lname = lname.replace(" ","_")
			contents.append('<div class="l2">' +
				'<a href="#%s">%s</a></div>' % 
				(lname,name) )
			doc.append( html.document( obj, name ) )
	
	contents.append("</td></tr></table>")
	
	h = html_template
	h = h.replace("%toc%", "".join(contents))
	h = h.replace("%contents%", "".join(doc))
	h = h.replace("%version%", templayer.__version__)
	print h

if __name__ == "__main__":
	main()
