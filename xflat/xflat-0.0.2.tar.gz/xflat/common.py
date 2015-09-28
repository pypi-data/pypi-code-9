
def escape(text):
    r = text
    r = text.strip()
    r = r.replace("\t"," ")
    r = r.replace("\r"," ")
    r = r.replace("\n"," ")
    r = r.strip("")
    return r

def unescape(text):
    r = text
    r = r.replace("\\t","\t")
    r = r.replace("\\r","\r")
    r = r.replace("\\n","\n")
    return r

def serialize_node(node, parents=[]):
    result = []
    attr = []
    level = []

    for k in sorted(node.attrib.keys()):
        v = node.attrib[k]
        vv = v.strip()
        r = "%s=\"%s\"" % (k.strip() ,v.strip())
        attr.append(r)

    my_name = node.tag
    if type(my_name) != type(""):
        my_name = "!"+ str(my_name).split(" ")[-1].strip("><").lower()
    me_included = parents + [my_name]
    name =  "/".join(me_included)
    text = node.text or ""

    depth = len(name.split("/"))
    row = "%s\t%s\t%s\t%s" % (name, escape(text), escape(node.tail or ""), " ".join(attr))
    result.append(row)
    for i in node:
        result.extend(serialize_node(i, me_included))
    return result

def attach_node(a, b):
    d =  b['level'] - a['level']
    if d == 1:
        a['children'].append(b)
    else:
        attach_node(a['children'][-1], b)

def str_node(a, pretty=False):
    result = ""
    if len(a['attrs']) > 0:
        result += u"<%(name)s %(attrs)s>%(content)s" % a
    else:
        result += "<%(name)s>%(content)s" % a
    for i in a['children']:
        result += str_node(i, pretty)
    if len(a['children']) > 0 or a['content']:
        result += "</%(name)s>" % a
    result += "%(tail)s" % a
    return result