from django import template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Variable, Node, NodeList, resolve_variable
from django.template import TemplateSyntaxError, VariableDoesNotExist

from changer.c5.menus.models import Menu, Link

register = template.Library()

@register.tag(name="get_menu")
def get_menu(parser, token):
    """
    Sets the variable links in the context, takes menutitle as string or variable argument
    """
    try:
        tag_name, format_string, = token.split_contents()
    except ValueError:
        msg = '%r tag requires arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        btype = True
    else:
        format_string = format_string[1:-1]
        btype = False
    return GetMenuNode(format_string, btype)

class GetMenuNode(template.Node):
    
    def __init__(self, format_string, btype=False, objmenu=None, strmenu=None):
        self.btype = btype
        self.objmenu = objmenu
        self.strmenu = strmenu
        
        if btype:
            self.objmenu = Variable(format_string)
        else:
            self.strmenu = format_string
    
    def render(self, context):
        if self.objmenu:
            _resolved = self.objmenu.resolve(context)
            try:
                menu = Menu.objects.get(title__icontains=_resolved.strip())
                links = menu.link_set.all()
                context["links"] = links
            except Menu.DoesNotExist:
                context["links"] = None
        elif self.strmenu:
            try:
                menu = Menu.objects.get(title__icontains=self.strmenu)
                links = menu.link_set.all()
                context["links"] = links
            except Menu.DoesNotExist:
                context["links"] = None
        return ''

@register.tag
def ifon(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 1:
        raise TemplateSyntaxError, "%r does not take arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfOnNode(nodelist_true,nodelist_false)

class IfOnNode(Node):
    def __init__(self,nodelist_true,nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
    
    def render(self, context):
        try:
            menuitem = resolve_variable('link', context)
        except VariableDoesNotExist:
            menuitem = None
        request = context['request']
        if request.path == menuitem.url:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

@register.tag
def ifchildon(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 1:
        raise TemplateSyntaxError, "%r does not take arguments" % bits[0]
    end_tag = 'end' + bits[0]
    
    #parse until either else or end_tag
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfChildOnNode(nodelist_true, nodelist_false)

class IfChildOnNode(Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
    
    def render(self, context):
        request = context['request']
        match = False
        
        #try to resolve link else return
        try:
            menuitem = resolve_variable('link', context)
        except VariableDoesNotExist:
            return self.nodelist_false.render(context)
        
        #try to find a menu and matching link url else match is false
        try:
            menu = Menu.objects.get(title__iexact=str(menuitem.title).strip())
        except Menu.DoesNotExist:
            menu = False
        else:
            link_urls = []
            for link in menu.link_set.all():
                if link.url == request.path:
                    link_urls.append(link.url)
                    match = True
            assert False, "%s , %s" % (link_urls, request.path)
        finally:
            if match:
                return self.nodelist_true.render(context)
            else:
                return self.nodelist_false.render(context)
