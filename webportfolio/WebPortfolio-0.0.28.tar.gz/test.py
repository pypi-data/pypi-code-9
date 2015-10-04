
from slugify import slugify

def create_slug(title):
    slug = None
    slug_counter = 0
    _slug = slugify(title).lower()
    while True:
        slug = _slug
        if slug_counter > 0:
            slug += str(slug_counter)
        slug_counter += 1
        if not get_by_slug(slug):
            break
    return slug

def get_by_slug(slug):
    return None

print create_slug("malta a lait")

exit()
def f():
    try:
        print "OK"
        return "Boom"
    except Exception as e:
        print e.message
    finally:
        print("Something is executed no matter what")

print f()

exit()

exit()
import re
regex = re.compile('[^a-zA-Z]')
print regex.sub('', 'vita_malt')

exit()

import functools
import inspect

class InspectDecoratorCompatibilityError(Exception):
    pass
class _InspectMethodsDecorators(object):

    def __init__(self, method):
        self.method = method
        self.decos = []

    def parse(self):
        self._parse(self.method)
        return list(set([deco for deco in self.decos if deco]))

    @classmethod
    def extract_deco(cls, line):
        line = line.strip()
        if line.startswith("@"):
            if "(" in line:
                line = line.split('(')[0].strip()
            return line.strip("@")

    def _parse(self, method):
        argspec = inspect.getargspec(method)
        args = argspec[0]
        if args and args[0] == 'self':
            return argspec
        if hasattr(method, '__func__'):
            method = method.__func__
        if not hasattr(method, '__closure__') or method.__closure__ is None:
            raise InspectDecoratorCompatibilityError

        closure = method.__closure__
        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                continue
            if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
                continue
            src = inspect.getsourcelines(inner_method)[0]
            self.decos += [self.extract_deco(line) for line in src]
            self._parse(inner_method)

def get_decorators_list(method):
    kls = _InspectMethodsDecorators(method)
    return kls.parse()


def test_get_decorators_list():

    def deco1(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            return func(*args, **kwargs)
        return decorated_view

    def deco2(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            return func(*args, **kwargs)
        return decorated_view

    class Hi(object):

        @deco1
        @deco2
        def hello(self):
            return True

    k_hi = Hi()
    decos = get_decorators_list(k_hi.hello)
    assert isinstance(decos, list)
    assert "deco1" in decos
    assert "deco2" in decos


test_get_decorators_list()
exit()



def parse_method_spec(method):
    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise InspectDecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
            and not inspect.ismethod(inner_method):
            continue
        src = inspect.getsourcelines(inner_method)[0]
        deco = [extract_decorator_line(line) for line in src]
        print deco
        true_argspec = parse_method_spec(inner_method)
        if true_argspec:
            return true_argspec






def login_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        print "LOGIN REQUIRED DECO"
        print get_decorators(func)
        return func(*args, **kwargs)
    return decorated_view

def no_login_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view

def jq(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view

import ast, inspect
def get_decorators2(target):

    res = {}
    def visit_FunctionDef(node):
        res[node.name] = [ast.dump(e) for e in node.decorator_list]
    print target.__code__
    #print inspect.getsource(target)
    V = ast.NodeVisitor()
    V.visit_FunctionDef = visit_FunctionDef
    #V.visit(compile(inspect.getsource(target), '?', 'exec', ast.PyCF_ONLY_AST))
    return res

class Hi(object):

    @login_required
    @jq
    @no_login_required
    def hello(self):
        print "Hello World"

h = Hi()
h.hello()

exit()
def user_is():
    return True
def user_can():
    return AttributeError

@user_is("Admin", "Login")
@user_permission("W")
def p():
    pass
exit()
total = 6
per_page = 2
page = 2

if total > per_page * page:
    print "Here"
    showing = per_page
else:
    print "THERE"
    showing = total - per_page * (page - 1)

showing = (total - per_page) * (page - 1)
print showing

exit()
import oembed

consumer = oembed.OEmbedConsumer()
endpoint = oembed.OEmbedEndpoint('http://www.flickr.com/services/oembed', \
                                 ['http://*.flickr.com/*'])
consumer.addEndpoint(endpoint)

response = consumer.embed('https://www.youtube.com/watch?v=BT5W4zllhCo')

print response['url']

import pprint
pprint.pprint(response.getData())


exit()
from webportfolio import wp_markdown

data = '''
[TOC]

#Header Palto
Got it
#Header Kila
I see what you did here

#Header Nice
###Kite li anle

**this is some markdown**

blah blah blah
![image here](http://somewebsite.com/image1.jpg)
![another image here](http://anotherwebsite.com/image2.jpg)
'''

print wp_markdown.html(data, lazy_images=True)

print wp_markdown.extract_images(data)

print wp_markdown.toc(data)
exit()

import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

# First create the treeprocessor

class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.markdown.images = []
        for image in doc.findall('.//img'):
            self.markdown.images.append(image.get('src'))

# Then tell markdown about it

class ImgExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        img_ext = ImgExtractor(md)
        md.treeprocessors.add('imgext', img_ext, '>inline')

# Finally create an instance of the Markdown class with the new extension

md = markdown.Markdown()

# Now let's test it out:

data = '''
**this is some markdown**
blah blah blah
![image here](http://somewebsite.com/image1.jpg)
![another image here](http://anotherwebsite.com/image2.jpg)
'''

html = md.convert(data)
#print html
print md.images


exit()
from six.moves.urllib.parse import urlencode, quote_plus, urlparse


d = urlparse("http://yahoo.com")
x = d.scheme == "https"
print x
exit()

a = {"hello": "world", "name":"whisky and I see"}
print quote_plus("Yo Mardix what's up")

print urlencode(a)

#a.update({"Joe": "Blow"})
#print a
exit()

endpoint_options={
     "read": {"nav_menu": "Documents", "route": "list", "show": False},
     "list": {"nav_menu": "Documents", "route": "list"},
     "archive": {"nav_menu": "Archive", "route": "archive"},
     "authors": {"nav_menu": "Authors", "route": "authors"}
 }






dn = DotDict(endpoint_options)
dn.location = "Charlotte"
dn.telephone.number.gamer = "910-551-7382"
print "Nice" if dn.joe else "Not Nice"

#print dn.joka.bo

print dn.get("archive.route.words", "No Nma")

#print dot_dict(endpoint_options, "archive.route.block.no_flex", "No name")

exit()
import re

# regular expression to match dates in format: 2010-08-27 and 2010/08/27
date_reg_exp = re.compile('\d{4}[/]\d{2}[/]\d{2}')

url_format_map = {
    "%slug": {
        "defaults": {
            "id": None,
            "date": None,
            "month": None
        },
        "pattern": "<regex('\d{4}[/]\d{2}[/]\d{2}'):date>/<slug>"
    },
    "%id-slug": {
        "defaults": {
            "date": None,
            "month": None
        },
        "pattern": "<regex('\d'):id>/<slug>"
    },
    "%date-slug": {
        "defaults": {
            "id": None,
            "month": None
        },
        "pattern": "<regex('\d{4}[/]\d{2}[/]\d{2}'):date>/<slug>"
    },
    "%month-slug": {
        "defaults": {
            "id": None,
            "date": None,
        },
        "pattern": "<regex('\d{4}[/]\d{2}[/]'):month>/<slug>"
    }
}




# a string to test the regular expression above
test_str= """
     fsf2010/08/27sdfsdfsd
     dsf sfds f2010/08/26 fsdf
     asdsds 2009-02-02 afdf
     """
# finds all the matches of the regular expression and
# returns a list containing them
matches_list=date_reg_exp.findall(test_str)

# iterates the matching list and prints all the matches
for match in matches_list:
  print match

exit()
d = {
    "<year>": "([0-9]{4})?",
    "<month>": "([0-9]{2})?",
    "<date>": "([0-9]{2})?",
    "<YMD>": "<year>/<month>/<date>"
}

s = "<year>/<month>/<date>"


pattern = re.compile('|'.join(d.keys()))
result = pattern.sub(lambda x: d[x.group()], s)

print result

exit()
def t():
    return False

a = [True, True, t]

print [x() if hasattr(x, "__call__") else x for x in a]

exit()
def is_auth():
    return is_a

def is_not_auth():
    return not is_a

print any([not is_a])
exit()
import pprint
from portfolio import Portfolio, nav_menu

@nav_menu("All", order=1)
class Index(Portfolio):

    @nav_menu("Home", order=1)
    def index(self):
        pass

    @nav_menu("Contact Us")
    def contact(self):
        pass

@nav_menu("My Account", order=2)
class Hello(Portfolio):
    
    @nav_menu("Hello World Index", __class="Index", order=2, title="The People People")
    def index(self):
        pass

    @nav_menu(name="More About us")
    def about(self):
        pass

app = Portfolio.init(__name__)

#pprint.pprint(Portfolio._nav_menu_stack)


exit()
import functools
import inspect
from flask_classy import FlaskView
from flask import Flask


__menu__ = []

app = Flask(__name__)

def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.__class__):
        if meth.__name__ in cls.__dict__:
            return cls
    return None


def menu(name, url=None, **kwargs):
    def wrap(f):
        print name
        print url
        print f.__module__
        print f.__name__

        #arg_spec = inspect.getargspec(f)
        #print arg_spec

        #print inspect.
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f
        return wrapper
    return wrap


class Index(FlaskView):

    @nav_menu("Home", url="Index:")
    def index(self):
        pass

    @nav_menu("Login")
    def index(self):
        pass

Index.register(app)



exit()
import functools
import inspect
import wrapt
from flask_classy import FlaskView




class Portfolio(object):
    @classmethod
    def extends_(cls, kls):
        if inspect.isclass(kls):
            for _name, _val in kls.__dict__.items():
                if not _name.startswith("__"):
                    setattr(cls, _name, _val)
        elif inspect.isfunction(kls):
            setattr(cls, kls.__name__, kls)
        return cls


class Q(Portfolio):
    def nice(self):
        return "NICE"

class P(Portfolio):
    def set_name(self, name):
        self.name = name

menu_list = []




p = P()
q = Q()
#print p.__dict__



@p.extends_
@nav_menu
def yo(self, name):
    self.set_name(name)
    print "I'm in self with %s in YO()  " % self.name


@p.extends_
@nav_menu("Home")
class A(object):
    phone = "123-2453-4343"
    CONST = 54

    @classmethod
    @nav_menu
    def c2(cls):
        return None

    def hello(self):
        print "This is hello"

    def index(self, name):
        self.set_name(name)
        print "I'm in self with %s " % self.name
        self.hello()

#print dir(p)
#print p.__dict__
p.hello()
p.yo("Koe")
p.index("Lola")
p.index("Nice One")

q.yo("Jones")
q.hello()
print p.phone
print p.CONST

#print f(name="Jones")
exit()

import functools

def deco(model, **kwargs):
    def wrapper(f):
        print f.__name__
        print model
        print kwargs
        return f
    return wrapper


@deco("my model", name="Jbeats")
class Global(object):
    pass


Global()
exit()




s1 = set([])
s2 = set(["B", "C", "W"])

deleted_s = s1 - s2
new_s = s2 - s1

print deleted_s
print new_s
temp3 = [x for x in s1 if x not in s2]

print temp3
exit()
from portfolio import utils

class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)

a = Struct(Name="Macxis", Location="Charlotte")

print a.Name
a.Name = "Jose"
print a.Name
print a.Location

print type(a)
def test_mailer_ses():
    pass

def Mailer():
    pass


mailer = Portfolio.bind_(Mailer.init_app())()



{% macro post_embed(post) %}
    {% if post.type == "video" or post.has_embed == true %}
        {% set url = post.url %}
        {% if post.has_embed %}
            {% set url = post.embed_url %}
        {% endif %}
        <div class="embed-responsive embed-responsive-16by9">
           <div class='embed-container'>
                {{ wp.oembed(url) }}
            </div>
        </div>
    {% else %}
        {{ post_top_image(post) }}
    {% endif %}
{% endmacro %}