#!/usr/bin/python

"""
Tutorial documentation generator for Templayer

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

from __future__ import nested_scopes

import sys
import os

import templayer

try: True # old python?
except: False, True = 0, 1

examples = {}
template = {}

interp_line = "#!/usr/bin/python\n\n"


template["lawn1"] = """
<html>
<head><title>Gordon's Lawn Happenings</title></head>
<body>
<h1>Gordon's Lawn Happenings</h1>
<h3>Sunday</h3>
<p>We've got a groundhog.  I will have to stay alert.</p>
<p>I lost half a tomato plant to that furry guy.</p>
<h3>Monday</h3>
<p>The grass grew - I saw it.</p>
</body>
</html>
"""

template["lawn2"] = """
<html>
<head><title>Gordon's Lawn Happenings</title></head>
<body>
<h1>Gordon's Lawn Happenings</h1>
{contents}

{/contents}
<h3>Sunday</h3>
<p>We've got a groundhog.  I will have to stay alert.</p>
<p>I lost half a tomato plant to that furry guy.</p>
<h3>Monday</h3>
<p>The grass grew - I saw it.</p>
</body>
</html>
"""

examples["lawn2"] = ["example_lawn2"]
def example_lawn2():
	import templayer
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	tmpl = templayer.HTMLTemplate("lawn2.html")
	file_writer = tmpl.start_file()
	file_writer.open()
	file_writer.close()

template["lawn3"] = """
<html>
<head><title>%title%</title></head>
<body>
<h1>%title%</h1>
{contents}

{/contents}
<h3>Sunday</h3>
<p>We've got a groundhog.  I will have to stay alert.</p>
<p>I lost half a tomato plant to that furry guy.</p>
<h3>Monday</h3>
<p>The grass grew - I saw it.</p>

<hr>
<p>Generated on %date%.</p>
</body>
</html>
"""

examples["lawn3"] = ["example_lawn3"]
def example_lawn3():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	tmpl = templayer.HTMLTemplate("lawn3.html")
	file_writer = tmpl.start_file()
	file_writer.open(title="Gordon's Lawn Happenings",
			date=time.asctime())
	file_writer.close()

template["lawn4"] = """
<html>
<head><title>%title%</title></head>
<body>
<h1>%title%</h1>
{contents}

{report}
<h3>%day%</h3>
%happenings%
{/report}

{/contents}
<hr>
<p>Generated on %date%.</p>
</body>
</html>
"""

examples["lawn4"] = ["example_lawn4a","example_lawn4b","example_lawn4c"]
def example_lawn4a():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	tmpl = templayer.HTMLTemplate("lawn4.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	main_layer.write_layer('report', day="Sunday", happenings=[
		"We've got a groundhog.  I will have to stay alert.",
		"I lost half a tomato plant to that furry guy."])
	main_layer.write_layer('report', day="Monday", happenings=[
		"The grass grew - I saw it."])
	file_writer.close()

def example_lawn4b():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', ["We've got a groundhog.  I will have to stay alert.",
		"I lost half a tomato plant to that furry guy."]),
		('Monday', ["The grass grew - I saw it."]),
	]

	tmpl = templayer.HTMLTemplate("lawn4.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		main_layer.write_layer('report', day=d, happenings=h)
	file_writer.close()

def example_lawn4c():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', [('p',"We've got a groundhog.  I will have to stay alert."),
			('p',"I lost half a tomato plant to that furry guy.")]),
		('Monday', [('p',"The grass grew - I saw it.")]),
	]

	tmpl = templayer.HTMLTemplate("lawn4.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		main_layer.write_layer('report', day=d, happenings=h)
	file_writer.close()

template["lawn5"] = """
<html>
<head><title>%title%</title></head>
<body>
<h1>%title%</h1>
{contents}

{report}
<h3>%day%</h3>
%happenings%
{/report}

{happening}<p>%what%</p>
{/happening}

{/contents}
<hr>
<p>Generated on %date%.</p>
</body>
</html>
"""

examples["lawn5"] = ["example_lawn5"]
def example_lawn5():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', ["We've got a groundhog.  I will have to stay alert.",
			"I lost half a tomato plant to that furry guy."]),
		('Monday', ["The grass grew - I saw it."]),
	]

	tmpl = templayer.HTMLTemplate("lawn5.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		happening_list = []
		for w in h:
			formatted = tmpl.format('happening', what=w)
			happening_list.append(formatted)
		main_layer.write_layer('report', day=d, happenings=happening_list)
	file_writer.close()

template["lawn6"] = """
<html>
<head><title>%title%</title></head>
<body>
<h1>%title%</h1>
{contents}

{report}
<h3>%day%</h3>
%contents%
{/report}

{happening}<p>%contents%</p>
{/happening}

{/contents}
<hr>
<p>Generated on %date%.</p>
</body>
</html>
"""

examples["lawn6"] = ["example_lawn6a","example_lawn6b","example_lawn6c"]
def example_lawn6a():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', ["We've got a groundhog.  I will have to stay alert.",
			"I lost half a tomato plant to that furry guy."]),
		('Monday', ["The grass grew - I saw it."]),
	]

	tmpl = templayer.HTMLTemplate("lawn6.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		report_layer = main_layer.open_layer('report', day=d)
		for happening in h:
			report_layer.write_layer('happening', contents=happening)
	file_writer.close()

def example_lawn6b():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', ["We've got a groundhog.  I will have to stay alert.",
			"I lost half a tomato plant to that furry guy."]),
		('Monday', ["The grass grew - I saw it."]),
	]

	tmpl = templayer.HTMLTemplate("lawn6.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		report_layer = main_layer.open_layer('report', day=d)
		for happening in h:
			happening_layer = report_layer.open_layer('happening')
			happening_layer.write(happening)
	file_writer.close()

def example_lawn6c():
	import templayer
	import time
	import sys

	sys.stdout.write("Content-type: text/html\r\n\r\n")

	reports = [
		('Sunday', ["We've got a groundhog.  I will have to stay alert.",
			"I lost half a tomato plant to that furry guy."]),
		('Monday', ["The grass grew - I saw it."]),
	]

	tmpl = templayer.HTMLTemplate("lawn6.html")
	file_writer = tmpl.start_file()
	main_layer = file_writer.open(title="Gordon's Lawn Happenings",
		date=time.asctime())
	for d, h in reports:
		report_layer = main_layer.open_layer('report', day=d)
		for happening in h:
			happening_layer = report_layer.open_layer('happening')
			happening_layer.write(happening)
		main_layer.close_child()
		file_writer.flush()
	file_writer.close()





template["simple.templayer"] = """
<html>
<head><title>%title%</title></head>
<body>

<h1>%title%</h1>
{contents}

{/contents}
</body>
</html>
"""

examples["simple.templayer"] = ["example_simple_views_1", "example_simple_views_2"]
def example_simple_views_1():
	from django.http import HttpResponse
	import datetime
	import templayer

	tmpl = templayer.get_django_template("simple.templayer.html")

	def current_datetime(request):
		file_writer = tmpl.start_file(HttpResponse())
		now = datetime.datetime.now()
		contents = file_writer.open(title="Current Date and Time")
		contents.write("It is now %s." % now)
		return file_writer.close()

def example_simple_views_2():
	import datetime
	import templayer

	tmpl = templayer.get_django_template("simple.templayer.html")

	@templayer.django_view(tmpl)
	def current_datetime(file_writer, request):
		now = datetime.datetime.now()
		contents = file_writer.open(title="Current Date and Time")
		contents.write("It is now %s." % now)

template["book.templayer"] = """
<html>
<head><title>%title%</title></head>
<body>

<h1>%title%</h1>
{contents}

{new_entry}
<form method="POST">
<h2>Sign the guestbook</h2>
Your Name: %form.name% %form.name.errors%<br/>
Rate the site: %form.rating% %form.rating.errors%<br/>
Your Comments:<br/>
%form.comment% %form.comment.errors%<br/>
<input type="submit" value="Submit"/>
</form>
{/new_entry}

{/contents}
</body>
</html>
"""

examples["book.templayer"] = ["example_book_models", "example_book_views"]
def example_book_models():
	from django.db import models

	RATING_CHOICES = (
		('G', "Great!"),
		('A', "Average"),
		('U', "Uninteresting"),
	)

	class Entry(models.Model):
		name = models.CharField("Your Name", max_length=100)
		rating = models.CharField("Rate this site", max_length=1,
			choices=RATING_CHOICES)
		comment = models.TextField("Your Comments (optional)", blank=True)
		posted = models.DateTimeField(auto_now_add=True)

def example_book_views():
	from book.models import Entry
	from django.forms import ModelForm

	import templayer

	tmpl = templayer.get_django_template("book.templayer.html")

	class EntryForm(ModelForm):
		class Meta:
			model = Entry

	@templayer.django_view(tmpl)
	def guest_book(file_layer, request):
		if request.POST:
			entry_form = EntryForm(request.POST)
			# TODO: do something with the data if all is well
		else:
			entry_form = EntryForm()
		contents = file_writer.open(title="Guest Book")
		contents.write_layer("new_entry", **templayer.django_form(entry_form))

template["emulate.templayer"] = """
<html>
<head><title>%title%</title></head>
<body>

<h1>%title%</h1>
{contents}

{show_404}
The url %url% could not be found.
{/show_404}

{flatpage_body}
%contents%
{/flatpage_body}

{/contents}
</body>
</html>
"""

examples["emulate.templayer"] = ["example_templayer_pages"]
def example_templayer_pages():
	import templayer

	tmpl = templayer.get_django_template("emulate.templayer.html")

	@templayer.django_template(tmpl, "404.html")
	def show_404(file_writer, context, request_path):
		contents = file_writer.open(title="Page not found")

		# request_path == context['request_path']
		contents.write_layer("show_404", url=request_path)

	@templayer.django_template(tmpl, "flatpages/default.html")
	def show_flatpage(file_writer, context, flatpage):
		contents = file_writer.open(title=flatpage.title)
		fp_contents = contents.open_layer("flatpage_body")

		# the flatpage content is HTML, so don't escape it.
		fp_contents.write(templayer.RawHTML(flatpage.content))




def read_sections(tmpl):
	"""Read section tags, section descriptions, and column breaks from
	the Templayer template argument.  Convert the section data into a
	Python data structure called sections.  Each sublist of sections
	contains one column.  Each column contains a list of (tag, desc.)
	pairs.  Return sections."""

	sd = tmpl.layer("section_data")
	col_break = "---"
	sections = [[]]
	for ln in sd.split("\n"):
		if not ln: continue
		if ln == col_break:
			sections.append([])
			continue
		tag, desc = ln.split("\t",1)
		sections[-1].append( (tag, templayer.RawHTML(desc)) )
	return sections

def read_example_code():
	"""By the time this function runs, the examples dictionary contains
	a list of function names, all starting with "example_".  Create a
	second dictionary called code_blocks.  Open the file containing this
	function.  For each function name in examples, read the text of that
	function into an entry in the code_blocks dictionary.  Return the
	code_blocks dictionary."""

	# invert the "examples" dictionary
	example_fns = {}
	for tag, l in examples.items():
		for i, fn in zip(range(len(l)), l):
			example_fns[fn] = tag, i
	
	# read our own source code
	# strip trailing spaces and tabs from each line
	code_blocks = {}
	current_block = None
	for ln in open( sys.argv[0], 'r').readlines():
		ln = ln.rstrip()
		if ( ln[:4] == "def " and ln[-3:] == "():" and
			example_fns.has_key( ln[4:-3] ) ):
			current_block = ln[4:-3]
			code_blocks[current_block] = []
			continue
		if ln and ln[:1] != "\t":
			current_block = None
			continue
		if current_block is None:
			continue
		if ln[:1] == "\t":
			ln = ln[1:]
		code_blocks[current_block].append(ln+"\n")
			
	# recombine code lines into a single string each
	for name, block in code_blocks.items():
		code_blocks[name] = "".join( block )
	
	return code_blocks


def write_example_files(sections, blocks):
	for t in template.keys():
		for e in examples.get(t, []):
			assert e.startswith("example_")
			open(e[8:]+".py", "w").write(blocks[e])
		open(t+".html", "w").write(template[t].lstrip())
	
			
class SimulatedOutput(object):
	output = []
	def write(self, s):
		self.output.append(s)

	def flush(self):
		pass

class NullOutput(object):
	def write(self, s):
		pass

		
def get_simulated_output():
	s = "".join(SimulatedOutput.output)
	del SimulatedOutput.output[:]
	return s


class SimulatedHTMLTemplate(templayer.HTMLTemplate):
	def __init__(self, name):
		name = name[:-len(".html")]
		t = template[name]
		head, t = t.split("<body>",1)
		t, tail = t.split("</body>",1)
		t = t.strip()
		self.encoding = "utf_8"
		self.set_template_data(template[name].decode(self.encoding))
	
	def start_file(self, file=None):
		return templayer.FileLayer(SimulatedOutput(), self)


def generate_results():
	"""
	Capture the output from the examples and return a dictionary 
	containing one result for each section that needs one.
	"""
	def get_result(fn):
		# divert the output to our simulated version
		orig_tmpl = templayer.HTMLTemplate
		orig_stdout = sys.stdout
		templayer.HTMLTemplate = SimulatedHTMLTemplate
		sys.stdout = NullOutput()
		
		fn()
		
		# restore the original values
		templayer.HTMLTemplate = orig_tmpl
		sys.stdout = orig_stdout
		
		return get_simulated_output()
		

	r = {}
	r['lawn1'] = [get_result(example_lawn2)]
	r['lawn3'] = [get_result(example_lawn3)]
	r['lawn4'] = [get_result(example_lawn4b), get_result(example_lawn4c)]

	return r


def generate_body(tmpl, sections, blocks):
	# put TOC columns into the variables used by the template
	# assign section numbers
	# generate HTML form of TOC entries, corresponding document parts
	assert len(sections) == 2, 'sections has %d columns but should have 2!' % len(sections)

	toc_slots = {'toc_left':[], 'toc_right':[]}
	body = []

	results = generate_results()
	
	snum = inum = 0
	for slot, l in zip(['toc_left','toc_right'], sections):
		for tag, name in l:
			if not tag:
				# new section -- do its first item next time
				snum += 1
				inum = 0
				t = tmpl.format('toc_section', snum=`snum`,
					name=name )
				toc_slots[slot].append( t )
				b = tmpl.format('section_head', snum=`snum`,
					name=name )
				body.append( b )
				continue

			# new item inside a section
			inum += 1
			t = tmpl.format('toc_item', snum=`snum`, 
				inum=`inum`, name=name, tag=tag)
			toc_slots[slot].append( t )

			slots = {}
			slots['html'] = tmpl.format('html_example',
				name = tag+".html",
				contents = template[tag])
			
			i = 0
			for fn in examples.get(tag, []):
				c = tmpl.format('code_example',
					name = fn[len("example_"):]+".py", 
					contents = blocks[fn])
				slots['code[%d]'%i] = c
				i += 1
			
			i = 0
			for r in results.get(tag, []):
				c = tmpl.format('result',
					contents = templayer.RawHTML(r))
				slots['result[%d]'%i] = c
				i += 1

			b = tmpl.format('body[%s]'%tag, ** slots )
			b = tmpl.format('section_body', snum=`snum`,
				inum=`inum`, name=name, tag=tag,
				contents = b)
			body.append( b )
			
	return (body, toc_slots)

def parse_options():
	usage = "%s [-h|-?|--help]\n%s [-H|--HTML|--html] [-s|--scripts]" % \
	 (sys.argv[0], sys.argv[0])
	help = """%s options:

-h, -?, --help		Print this message to standard error and exit.

-H, --HTML, --html	Write the HTML documentation to standard output.
-s, --scripts		Write runnable scripts to files.""" % sys.argv[0]
	do_html = False
	do_scripts = False

	if len(sys.argv) < 2 or len(sys.argv) > 3:
		sys.exit(usage)

	if len(sys.argv) == 2 and (sys.argv[1] in ('-h', '-?', '--help')):
		sys.exit(help)

	for arg in sys.argv[1:]:
		if arg in ('-H', '--HTML', '--html'):
			if do_html:	sys.exit(usage)
			else:		do_html = True
		elif arg in ('-s', '--scripts'):
			if do_scripts:	sys.exit(usage)
			else:		do_scripts = True
		else:
			sys.exit(usage)

	return (do_html, do_scripts)

def main():
	(do_html, do_scripts) = parse_options()

	tmpl = templayer.HTMLTemplate(
		os.path.join(os.path.dirname(sys.argv[0]),
		"tmpl_tutorial.html"))
	sections = read_sections( tmpl )
	code_blocks = read_example_code()

	if do_scripts:
		write_example_files( sections, code_blocks )

	if do_html:
		out_file = tmpl.start_file()
		(body, toc_slots) = generate_body( tmpl, sections,
		                                   code_blocks )
		bottom = out_file.open(version=templayer.__version__,
			** toc_slots)
		bottom.write( body )
		out_file.close()

if __name__=="__main__":
	main()
