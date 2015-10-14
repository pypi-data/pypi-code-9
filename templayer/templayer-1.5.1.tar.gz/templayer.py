#!/usr/bin/python

"""
templayer.py - Layered Template Library for HTML

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

__author__ = "Ian Ward"
__version__ = "1.5.1"

import string
import sys
import os
import time
import re
from types import TupleType, ListType, IntType, UnicodeType
from inspect import getargspec

try: True # old python?
except: False, True = 0, 1

SLOT_MARK = "%"
BEGIN_MARK = "{"
END_MARK = "}"
CLOSE_PREFIX = "/"
CONTENTS = "contents"
CONTENTS_OPEN = BEGIN_MARK+CONTENTS+END_MARK
CONTENTS_CLOSE = BEGIN_MARK+CLOSE_PREFIX+CONTENTS+END_MARK
COMPLETE_FILE_LAYER = "*"

ENTITY_RE = re.compile("^#x[0-9A-Fa-f]+$|^#[0-9]+$|^[a-zA-Z]+$")

TEMPLAYER_PAGES_MODULE = "templayer_pages"

class TemplateError(Exception):
	pass

class Template(object):
	"""
	class Template - common functionality for Template subclasses
	"""
	def __init__( self, name, from_string=False, auto_reload='never',
		allow_degenerate=False, encoding='utf_8'):
		"""
		name -- template file name or file-like object
		from_string -- if True treat name as a string containing the
		               template data instead of a file to read from
		auto_reload -- if the template has not been checked in this
		               many seconds then check it and reload if there
			       are any changes.  If 'never' only load the 
			       template file once.

			       Checking and reloading is done by the 
			       start_file() function.
			       
			       Ignored if from_string is True or if name is a 
			       file-like object.
		allow_degenerate -- If True then template is allowed to not
		               have a {contents}...{/contents} block.  In this
			       case the entire file is available as a layer
			       called '*'.  eg. l = tmpl.format('*', ...)
		encoding -- encoding for template file
		"""
		
		self.allow_degenerate = allow_degenerate
		self.encoding = encoding
		self.auto_reload = auto_reload
		self.template_ts = 0

		self.template_name = None
		if from_string:
			data = name
			if type(data)!=UnicodeType:
				data = data.decode(encoding)
			self.set_template_data(data)
			auto_reload = None
		elif hasattr(name, "read"):
			self.set_template_data(name.read().decode(encoding))
			auto_reload = 'never'
		else:
			self.template_name = name
			self.reload_template()

		
	
	def reload_template(self):
		"""Reload the template data from the template file."""
		if not self.template_name: return
		tmpl = open(self.template_name).read().decode(self.encoding)
		self.set_template_data(tmpl)

	def template_file_changed(self):
		"""
		Return True if the template file has been modified since
		the last time it was loaded.
		"""
		if self.template_ts == "never":
			return False
		if not self.template_name:
			return True # we don't know if it has changed
		if os.stat(self.template_name)[8] != self.template_ts:
			return True

	def set_template_data(self,tmpl):
		"""Parse and store the template data passed."""
		if type(tmpl) != UnicodeType:
			raise TemplateError("template data must be "
				"a unicode string")

		self.cache = {}
		try:
			# use the first CONTENTS_BEGIN in the file
			header, rest = tmpl.split(CONTENTS_OPEN,1)
			# and the last CONTENTS_CLOSE in the file
			rest_l = rest.split(CONTENTS_CLOSE)
			if len(rest_l)<2:
				raise ValueError
			footer = rest_l[-1]
			body = CONTENTS_CLOSE.join(rest_l[:-1])
			self.contents_open = CONTENTS_OPEN
			self.contents_close = CONTENTS_CLOSE
			
		except ValueError:
			if not self.allow_degenerate:
				raise TemplateError, "Template Contents Block "\
					"Missing: %s...%s" % \
					(CONTENTS_OPEN, CONTENTS_CLOSE )
			# degenerate template
			header = tmpl
			footer = body = ""
			self.contents_open = self.contents_close = ""
		
		self.header = header.split(SLOT_MARK)
		self.footer = footer.split(SLOT_MARK)
		self.body = []
		body_l = body.split(BEGIN_MARK)
		for b in body_l:
			self.body.append( b.split(SLOT_MARK) )

	def layer_split( self, name ):
		"""Return the layer named name split on SLOT_MARKs."""
		if BEGIN_MARK in name or SLOT_MARK in name:
			raise TemplateError, "Layer names cannot include %s " \
				"or %s" % (BEGIN_MARK, SLOT_MARK)
		if name == COMPLETE_FILE_LAYER:
			begin = 0
			end = len(self.body)
		elif self.cache.has_key(name): 
			begin, end = self.cache[name]
		else:
			begin = None
			end = None
			i = 1
			for b in self.body[1:]:
				if begin is None \
					and b[0].startswith(name+END_MARK):
					begin = i
				if begin is not None and b[0].startswith(
					CLOSE_PREFIX+name+END_MARK):
					end = i
				i += 1
			if end is None or begin is None:
				raise TemplateError, "Template Layer Missing:"\
					" %s...%s"%(BEGIN_MARK+name+END_MARK,
					BEGIN_MARK+CLOSE_PREFIX+name+END_MARK)
			self.cache[name] = begin, end

		o = []
		for i in range(begin, end):
			b = self.body[i]
			if o:
				# join across BEGIN_MARKs
				o[-1] = o[-1]+BEGIN_MARK+b[0]
				o.extend(b[1:])
			else:
				o.extend(b)
		
		if name == COMPLETE_FILE_LAYER:
			# include the header and footer
			c = self.header[:-1]
			c.append(self.header[-1] + self.contents_open + o[0])
			c.extend(o[1:])
			c[-1] = c[-1] + self.contents_close + self.footer[0]
			c.extend(self.footer[1:])
			o = c
		else:
			# remove the opening layer tag
			o[0] = o[0][len(name)+len(END_MARK):]
			
		return o
		

	def layer( self, name ):
		"""Return the complete layer named name as a string."""
		return SLOT_MARK.join(self.layer_split(name))

	def missing_slot(self, names, layer):
		"""Called when one or more slots are not found in a layer."""
		if layer is None:
			where = "Header/Footer"
		else:
			where = "Layer %s" % (BEGIN_MARK+layer+END_MARK)
		
		slots = [SLOT_MARK+name+SLOT_MARK for name in names]
		if len(slots)>1:
			slotp = "slots"
		else:
			slotp = "slot"

		raise TemplateError, "%s is missing the following %s: %s" % (
			where, slotp, ", ".join(slots))

			
	def format_header_footer( self, **args ):
		"""Returns header and footer with slots filled by args."""
		fargs = {}
		for k, v in args.items():
			k, v = self.pre_process(k, v)
			fargs[k] = v
		
		header, missing_h = fill_slots(self.header, **fargs)
		footer, missing_f = fill_slots(self.footer, **fargs)
		
		d = {}
		for m in missing_h:
			d[m] = True
		missing = [m for m in missing_f if d.has_key(m)]
		
		if missing:
			self.missing_slot(missing, None)
		
		return self.post_process(header), self.post_process(footer)


	def format( self, layer_name, ** args ):
		"""
		Return a layer with slots filled by args.
		
		self.format(...) and self(...) are equivalent.
		"""
		s = self.layer_split(layer_name)

		fargs = {}
		for k, v in args.items():
			k, v = self.pre_process(k, v)
			fargs[k] = v

		s, missing = fill_slots(s, **fargs)

		if missing:
			self.missing_slot(missing, layer_name)
		
		return self.post_process(s)
	
	__call__ = format

	def start_file( self, file=None, encoding='utf_8' ):
		"""
		Return a FileWriter object that uses this template.

		file -- file object or None to use sys.stdout.
		
		If self.auto_reload is not None this function will first 
		check and reload the template file if it has changed.
		"""
		if self.auto_reload is not None:
			t = time.time()
			if self.auto_reload != "never" and \
				t > self.template_ts+self.auto_reload:
				if self.template_file_changed():
					self.reload_template()
				self.template_ts = t
		
		return FileWriter( file, self, encoding )

	def pre_process( self, key, value ):
		"""
		Returns key, filtered/escaped value.

		Override this function to provide escaping or filtering of
		text sent from the module user.
		"""
		return key, value
	
	def post_process( self, value ):
		"""
		Returns wrapped value.

		Override to wrap processed text in order to mark it as 
		having been processed.
		"""
		return value
		
	def finalize( self, value ):
		"""
		Return unwrapped value as a string.
		
		Override this function to reverse wrapping applied before
		sending to the output file.
		"""
		return value


def fill_slots(layer_split, **args):
	"""Return layer_split filled with args, missing slot list."""
	filled = {}
	o = []
	last_is_slot = True
	for p in layer_split[:-1]:
		if last_is_slot:
			last_is_slot = False
			o.append(p)
		elif args.has_key(p):
			o.append(unicode(args[p]))
			filled[p] = True
			last_is_slot = True
		else:
			o.extend([SLOT_MARK,p])
	if not last_is_slot:
		o.append(SLOT_MARK)
	o.append(layer_split[-1])
	
	missing = []
	if len(filled)<len(args):
		missing = [n for n in args.keys() if not filled.has_key(n)]
	return "".join(o), missing


class HTMLTemplate(Template):
	"""
	Treats input to write and write_layer as "markup" defined by 
	expand_html_markup()
	"""
	def pre_process(self, key, value):
		"""
		Use expand_html_markup to process value.
		"""
		return key, expand_html_markup(value)
		
	def post_process(self, value ):
		"""
		Wrap value in RawHTML object.
		"""
		return RawHTML( value )
		
	def finalize(self, value):
		"""
		Unwrap RawHTML object value for output.
		"""
		assert isinstance(value,RawHTML)
		return value.value

# backwards compatibility
HtmlTemplate = HTMLTemplate




class MarkupError(Exception):
	pass
# backwards compatibility
MarkupException = MarkupError

MKE_BAD_TYPE = "Expecting string, list, tuple or RawHTML, but found %s"
MKE_INVALID_HREF = "'href' must be in the form ('href',url,content) or " \
	"('href',('urljoin',head,tail),content)"
MKE_INVALID_JOIN = "'join' must be in the form ('join',list,separator)"
MKE_INVALID_PLURALIZE = "'pluralize' must be in the form " \
	"('pluralize',count,singular_content,plural_content)"
MKE_INVALID_URLJOIN = "'urljoin' must be in the form ('urljoin',safe_str," \
	"unsafe_str)"
MKE_INVALID_TARGET = "'target' must be in the form ('target',name,contents)"
MKE_INVALID_BR_P = "'%s' must be in the form ('%s',) or ('%s',count)"
MKE_INVALID_B_I_U = "'%s' must be in the form ('%s',content)"
MKE_INVALID_ENTITY = "'&' must be the form ('&',entity) where valid entity " \
	"values include: 'gt', '#161' and '#xA9'."
MKE_UNRECOGNISED = "tuple must begin with one of the following strings: " \
	"'join', 'urljoin', 'href', 'target', 'br', 'p', 'i', 'b'"


def join(markup_list, separator):
	"""HTML Markup like markup_list.join(separator)"""
	return expand_html_markup(('join', markup_list, separator))
def pluralize(count, sigular_content, plural_content):
	"""HTML Markup (singular_content if count==1 else plural_content)"""
	return expand_html_markup(
		('pluralize', count, singular_content, plural_content))
def urljoin(head, tail):
	"""HTML Markup join safe url head with unsafe tail"""
	return expand_html_markup(('urljoin', head, tail))
def href(link, content):
	"""HTML Markup <a href="link">content</a>"""
	return expand_html_markup(('href', link, content))
def target(name):
	"""HTML Markup <a name="name"></a>"""
	return expand_html_markup(('target', name))
def BR(count=1):
	"""HTML Markup <br/> * count"""
	return expand_html_markup(('br', count))
def P(content=""):
	"""HTML Markup <p>content</p>"""
	return expand_html_markip(('p', content))
def I(content):
	"""HTML Markup <i>content</i>"""
	return expand_html_markip(('i', content))
def B(content):
	"""HTML Markup <b>content</b>"""
	return expand_html_markip(('b', content))
def U(content):
	"""HTML Markup <u>content</u>"""
	return expand_html_markip(('u', content))
def entity(entity):
	"""HTML Markup &entity;"""
	return expand_html_markip(('&', entity))


def expand_html_markup( v ):
	"""
	Return an HTML string based on markup v.

	HTML markup is expanded recursively. Each of the content
	values below are passed to expand_html_markup again before 
	applying the operation on the right:
	
	string or unicode string    ->  HTML-escaped version of string
	[content1, content2, ...]   ->  concatenate content1, content2, ...
	('join',list,sep)     ->  join items in list with seperator sep
	('pluralize',count,singular_content,plural_content)
	                      ->  if count == 1 use singular_content,
			          otherwise use plural_content
	('urljoin',head,tail) ->  join safe url head with unsafe url-ending tail
	('href',link,content) ->  HTML href to link wrapped around content
	('target',name)       ->  HTML target name
	('br',)               ->  HTML line break
	('br',count)          ->  HTML line break * count
	('p',)                ->  HTML paragraph break
	('p',content)         ->  HTML paragraph
	('i',content)         ->  italics
	('b',content)         ->  bold
	('u',content)         ->  underline
	('&',entity)          ->  HTML entity (entity has no & or ;)
	RawHTML(value)        ->  value unmodified
	"""
	if isinstance(v,RawHTML):
		return v.value
		
	if type(v) == ListType:
		l = []
		for x in v:
			l.append( expand_html_markup( x ) )
		return "".join(l)

	if type(v) != TupleType:
		try:
			return html_escape(v)
		except AttributeError, err:
			raise MarkupError(MKE_BAD_TYPE % repr(type(v)))
	
	if v[0] == 'href':
		if len(v)!=3:
			raise MarkupError(MKE_INVALID_HREF)
		if type(v[1]) != TupleType or v[1][0]!='urljoin':
			v=[ v[0], ('urljoin',v[1],"") ,v[2] ]
		return html_href(expand_html_markup(v[1]),
			expand_html_markup(v[2]))
		
	if v[0] == 'join':
		if len(v)!=3 or type(v[1]) != ListType:
			raise MarkupError(MKE_INVALID_JOIN)
		sep = expand_html_markup(v[2])
		l = []
		for x in v[1]:
			l.append( expand_html_markup( x ) )
		return sep.join(l)
	
	if v[0] == 'pluralize':
		if len(v)!=4:
			raise MarkupError(MKE_INVALID_PLURALIZE)
		if v[1]==1:
			return expand_html_markup(v[2])
		else:
			return expand_html_markup(v[3])
		
	if v[0] == 'urljoin':
		if len(v)!=3:
			raise MarkupError(MKE_INVALID_URLJOIN)
		try:
			return v[1]+html_url_encode(v[2])
		except TypeError, err:
			raise MarkupError(MKE_INVALID_URLJOIN)
		except AttributeError, err:
			raise MarkupError(MKE_INVALID_URLJOIN)
	
	if v[0] == 'target':
		if len(v)!=3:
			raise MarkupError(MKE_INVALID_TARGET)
		return html_target(html_url_encode(v[1]),
			expand_html_markup(v[2]))
			
	if v[0] == 'p' and len(v) == 2 and type(v[1]) != IntType:
		return "<p>"+expand_html_markup(v[1])+"</p>"
		
	if v[0] == 'br' or v[0] == 'p':
		if len(v)==1:
			v = (v[0], 1)
		if len(v)!=2 or type(v[1]) != IntType:
			raise MarkupError(MKE_INVALID_BR_P %(v[0],v[0]))
		return ("<"+v[0]+"/>") * v[1]
		
	if v[0] == 'b' or v[0] == 'i' or v[0] == 'u':
		if len(v)!=2:
			raise MarkupError(MKE_INVALID_B_I_U %(v[0],v[0]))
		return ("<"+v[0]+">"+
			expand_html_markup(v[1])+
			"</"+v[0]+">")
	
	if v[0] == '&':
		if len(v)!=2:
			raise MarkupError(MKE_INVALID_ENTITY)
		if not ENTITY_RE.match(v[1]):
			raise MarkupError(MKE_INVALID_ENTITY)
		return "&"+v[1]+";"

	raise MarkupError(MKE_UNRECOGNISED)


class RawHTML(object):
	"""
	class RawHTML - wrap strings of generated html that are passed 
	outside the module so that they aren't escaped when passed back in
	"""
	def __init__( self, value ):
		"""value -- segment of HTML as a string"""
		self.value = value
	def __repr__( self ):
		return 'RawHTML(%s)'%repr(self.value)


class LayerError(Exception):
	pass

class FileWriter(object):
	"""
	class FileWriter - the layer within which all other layers nest,
	responsible for sending generated text to the output stream
	"""
	def __init__( self, file, template, encoding='utf_8' ):
		"""
		file -- output stream or None to use sys.stdout
		template -- template object for generating this file

		This constructor is usually not called directly.  Use
		template.start_file() to create a FileWriter instead.
		"""
		if not file: file = sys.stdout
		self.out = file
		self.template = template
		self.child = None
		self.encoding = encoding
	
	def open( self, ** args ):
		"""
		Return a new layer representing the content between the
		header and footer.  Use keyword arguments to fill the
		slots in the header and footer.
		"""
		assert self.child == None
		header, footer = self.template.format_header_footer(**args)
		
		self.child = Layer( self.template, header, footer )
		return self.child
	
	def flush( self ):
		"""
		Flush as much output as possible to the output stream.
		"""
		assert self.child != None, "FileWriter already closed!"
		data ="".join(self.child.flush())
		self.out.write(data.encode(self.encoding))
		self.out.flush()
	
	def close( self ):
		"""
		Close all child layers and flush the output to the output 
		stream.  This function must be called to generate a complete
		file.

		Returns the file object where output was sent.
		"""
		assert self.child != None, "FileWriter.close() already called "\
			"or .open() was never called!"
		data ="".join(self.child.close())
		self.out.write(data.encode(self.encoding))
		self.child = None
		return self.out

# backwards compatibility	
FileLayer = FileWriter


class Layer(object):
	"""
	class Layer - holds the state of one of the nested layers while its
	contents are being written to.  Layers are closed implicitly when
	a parent layer is written to, or explicitly when its parent's
	close_child is called.
	"""
	def __init__( self, template, header, footer ):
		"""
		template -- template object for generating this layer
		header -- text before the content of this layer
		footer -- text after the content of this layer

		This constructor should not be called directly.  Use
		the open() function in a FileWriter or the open_layer()
		function in another Layer object to create a new Layer.
		"""
		self.child = None
		self.template = template
		header = self.template.finalize(header)
		self.out = [header]
		self.footer = self.template.finalize(footer)
	
	def close_child(self):
		"""
		If we have an open child layer close it and add its
		output to our own.
		"""
		if self.out == None:
			raise LayerError, "Layer is closed!"
		if self.child:
			self.out = self.out + self.child.close()
			self.child = None
	
	def open_layer( self, layer, ** args ):
		"""
		layer -- name of layer in the template to open
		Use keyword arguments to fill this layer's slots.
		
		open_layer( layer name, ** args ) -> child Layer object

		open a layer as a child of this one, filling its slots with
		values from args
		"""
		c = SLOT_MARK+CONTENTS+SLOT_MARK
		if args.has_key(CONTENTS):
			raise LayerError, "Cannot specify a value for " + \
				c+" when calling open_layer(). Use " + \
				"write_layer() instead."
		block = self.template.format( layer, ** args )
		l = block.value.split(c)
		if len(l) == 1:
			raise LayerError, "Cannot open layer " + \
				BEGIN_MARK+layer+END_MARK+" because it is " + \
				"missing a "+c+" slot."
		if len(l) > 2:
			raise LayerError, "Cannot open layer " + \
				BEGIN_MARK+layer+END_MARK+" because it has " + \
				"more than one "+c+" slot."
		header, footer = l
		self.close_child()
		header = self.template.post_process(header)
		footer = self.template.post_process(footer)
		self.child = Layer( self.template, header, footer)
		return self.child

	def write_layer( self, layer, ** args ):
		"""
		layer -- name of layer in the template to write
		Use keyword arguments to fill this layer's slots.
		"""
		self.close_child()
		result = self.template.format( layer, ** args )
		self.out.append( self.template.finalize(result) )
	
	def write( self, text ):
		"""
		text -- text or markup as interpreted by the template
		"""
		ignore, result = self.template.pre_process("",text)
		result = self.template.post_process(result)
		self.close_child()
		self.out.append( self.template.finalize(result) )

	def flush( self ):
		"""
		Flush as much output as possible and return it.

		This function should not be called directly.  Use the
		flush() function in the FileWriter object instead.
		"""
		if self.out == None:
			raise LayerError, "Layer is closed!"
		output = self.out 
		if self.child:
			output = output + self.child.flush()
		self.out = []
		return output

	def close( self ):
		"""
		Close this layer and return its output.
		
		This function should not be called directly.  Use the
		close() function in the FileWriter object instead.
		"""
		self.close_child()
		final = self.out+[self.footer]
		self.out = None # break further outputting
		return final
		

_html_url_valid = string.letters + string.digits + "$-_.!*'()"
def html_url_encode(text, query=False):
	"""
	text -- text to be included as part of a URL
	query -- if True use "+" instead ot "%20" for spaces
	"""
	
	url = ""
	for c in text:
		if c in _html_url_valid:
			url += c
		elif query and c==" ":
			url += "+"
		else:
			url += "%" + "%02x" % ord(c)
	return url

def html_href(link,value):
	"""
	Return '<a href="link">value</a>'.
	
	Neither link nor value is escaped by this function.
	"""
	
	return '<a href="%s">%s</a>'%(link,value)

def html_target(target,caption):
	"""
	Return '<a name="target">caption</a>'.
	
	Neither target nor caption is escaped by this function.
	"""
	
	return '<a name="%s">%s</a>'%(target,caption)


def html_escape(text):
	"""
	text -- text to be escaped for inclusion within HTML.
	"""

	text = text.replace('&','&amp;')
	text = text.replace('"','&quot;') # in case we're in an attrib.
	text = text.replace('<','&lt;')
	text = text.replace('>','&gt;')
	return text


def django_form(form, errors=True, join_errors=lambda x: ('join', x, ('br,'))):
	"""
	Converts a django FormWrapper object to a dictionary that
	can be used by Templayer.  Each field is rendered into a
	%form.NAME% slot.

	If errors is True then this function will also render
	errors into %form.NAME.errors% slots.

	When there is more than one error on a single field the
	errors will be joined with the join_errors function.
	The default join_errors function puts a newline between each
	error.

	eg:
	If tmpl is an HTMLTemplate object with a {form_layer} layer
	and form is a FormWrapper object with username and password
	fields, then this code will fill the {form_layer} layer's 
	%title%, %form.username%, %form.password%, 
	%form.username.errors% and %form.password.errors% slots:
	
	tmpl.format('form_layer', title="hello", **django_form(form))
	"""
	d = {}
	for field_name in form.fields:
		value = form[field_name]
		d["form."+field_name] = RawHTML(str(value))
		if errors:
			e = [x for x in form.errors.get(field_name,[])]
			d["form." + field_name + ".errors"] = join_errors(e)
	return d



class DjangoTemplayerError(Exception):
	pass

class _DjangoTemplayer(object):
	def __init__(self, run, template_name, tmpl, args, optargs):
		self.run = run
		self.template_name = template_name
		self.tmpl = tmpl
		self.args = args
		self.optargs = optargs

	def render(self, context_instance):
		from django.http import HttpResponse

		sendargs = {}
		for arg in self.args:
			if arg not in context_instance:
				raise DjangoTemplayerError("Required "
					"parameter %s was not passed to "
					"template %s!" % (
					repr(arg), repr(self.template_name)))
			sendargs[arg] = context_instance[arg]
		for arg in self.optargs:
			if arg in context_instance:
				sendargs[arg] = context_instance[arg]

		# create the file layer before calling our function
		fwriter = self.tmpl.start_file(HttpResponse())
		response = self.run(fwriter, context_instance, **sendargs)
		# if the file layer (or None) is returned, render it
		if response is fwriter or response is None:
			response = fwriter.close()
		return response.content


_django_templates = {}
_django_templates_searched = False

def django_template_loader(template_name, template_dirs=None):
	"""
	This function should be included in settings.TEMPLATE_LOADERS when
	using the django_template decorator.

	eg:
	TEMPLATE_LOADERS += ['templayer.django_template_loader']
	"""
	global _django_templates
	global _django_templates_searched

	from django.template import TemplateDoesNotExist

	if template_name not in _django_templates and \
		not _django_templates_searched:
		_django_templates_searched = True
		# django template registration is a side-effect of importing
		# a module with django_template decorators, so try
		# looking in the views modules of installed applications
		
		from django.conf import settings
		targets = []
		for droot in settings.TEMPLATE_DIRS:
			for d, subdirs, files in os.walk(droot):
				if TEMPLAYER_PAGES_MODULE+".py" in files:
					targets.append(d)

		for t in targets:
			orig_sys_path = sys.path
			try:
				sys.path = [t] + orig_sys_path
				__import__(TEMPLAYER_PAGES_MODULE)
			finally:
				sys.path = orig_sys_path

	if template_name not in _django_templates:
		raise TemplateDoesNotExist()

	run, tmpl, args, optargs = _django_templates[template_name]
	return (_DjangoTemplayer(run, template_name, tmpl, args, optargs),
		# make a pretend template name based on the file/fn name
		run.func_code.co_filename + "." + run.func_code.co_name)

# This oddity is reqired for Django template loaders:
django_template_loader.is_usable = True


def django_template(tmpl, template_name):
	"""
	This is a decorator for functions you want to make behave like 
	standard Django templates.  When django_template_loader is 
	included in settings.TEMPLATE_LOADERS Django will find the 
	decorated function when looking for template_name.

	tmpl is the Templayer template object that will be used to create
	the file layer passed to the decorated function.

	The decorated function must have a signature like:
	@templayer.django_template(tmpl, "appname/somepage.html")
	def mock_template(fwriter, context, optional1, optional2 ...)
	
	Where fwriter is a new FileWriter object, context is a context
	instance and all parameters that follow will have their values
	copied from the context based on the name of the parameters.

	The function must call fwriter.open(..) to render the page then 
	return the fwriter object (or None) to send it to the client.  
	fwriter.close() is called automatically.  Other objects returned 
	or exceptions raised will be passed through to Django.
	"""
	global _django_templates

	if not _django_templates:
		_hook_django_template_loading()
	
	def register_mock_template(fn):
		args, varargs, varkw, defaults = getargspec(fn)
		if len(args) < 2:
			raise DjangoTemplayerError("django_template()-"
				"decorated functions must have fwriter "
				"and context as their first two parameters")

		nonoptional = len(args) - len(defaults or ())
		args, optargs = args[2:nonoptional], args[min(2,nonoptional):]
		_django_templates[template_name] = (fn, tmpl, args, optargs)
		return fn
	return register_mock_template

def _hook_django_template_loading():
	import django.template.loader
	orig_gtfs = django.template.loader.get_template_from_string

	def get_template_from_string(source, *largs, **dargs):
		if isinstance(source, _DjangoTemplayer):
			return source
		return orig_gtfs(source, *largs, **dargs)

	django.template.loader.get_template_from_string = get_template_from_string


def django_view(tmpl):
	"""
	This is a decorator for Django view functions that will handle
	creation of the file layer object from the template tmpl.

	The function must have a signature like:
	@templayer.django_view(tmpl)
	def decorated_view(fwriter, request, ...)

	fwriter is the new FileWriter object and the rest of the parameters
	are the same as what was passed to the view.  
	
	The function must call fwriter.open(..) to render the page then 
	return the fwriter object (or None) to send it to the client.  
	fwriter.close() is called automatically.  Other objects returned 
	or exceptions raised will be passed through to Django.
	"""
	from django.http import HttpResponse
	
	def view_wrapper(fn):
		def wrapped_view(request, *argl, **argd):
			# create the file layer before calling our function
			fwriter = tmpl.start_file(HttpResponse())
			response = fn(fwriter, request, *argl, **argd)
			# if the file layer (or None) is returned, render it
			if response is fwriter or response is None:
				response = fwriter.close()
			return response

		# do our best to make the decorated function resemble the 
		# original function
		wrapped_view.__name__ = fn.__name__
		wrapped_view.__dict__.update(fn.__dict__)
		wrapped_view.__doc__ = fn.__doc__
		wrapped_view.__module__ = fn.__module__
		return wrapped_view

	return view_wrapper


def get_django_template(name, auto_reload='debug', allow_degenerate=False, 
	encoding='utf_8'):
	"""
	Use Django's template loading machinery to create an
	HTMLTemplate object.

	auto_reload -- when set to 'debug' will auto-reload only when 
		settings.DEBUG is set to True
	"""
	from django.template.loader import find_template_source

	source, obj = find_template_source(name)

	if auto_reload == 'debug':
		from django.conf import settings
		if settings.DEBUG:
			auto_reload = 0
		else:
			auto_reload = 'never'

	tmpl = HTMLTemplate(source, from_string=True, 
		auto_reload=auto_reload, encoding=encoding)
	return tmpl


if __name__ == "__main__": main()
