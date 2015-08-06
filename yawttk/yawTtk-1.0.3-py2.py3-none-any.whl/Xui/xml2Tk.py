# -*- coding:utf-8 -*-
import os, sys, warnings #, functools, 
from . import getXmlDom

# root node = <Xui return=list[|Tk|Toplevel] **{param=value}></Xui>

LAYOUT_KEYS = {
	"grid":  ["column", "columnspan", "padx", "pady", "row", "rowspan", "sticky"],
	"pack":  ["after", "anchor", "before ", "expand", "fill", "padx", "pady", "side"],
	"place": ["anchor", "bordermode", "height", "relheight", "relwidth", "relx", "rely", "width", "x", "y"],
} # "in" parameter is common to all !

def searchWidget(widget, name):
	for child in widget.children:
		if child == name:
			return widget.children[child]
		else:
			w = searchWidget(widget.children[child], name)
			if w != False: return w
	return False

def listEtree(obj):
	try: return list(obj)
	except: return obj.getchildren()

def stripLayout(element):
	for key in ["grid", "place", "pack"]:
		params = dict((k,element.attrib.pop(k)) for k in list(element.attrib.keys()) if k in LAYOUT_KEYS[key])
		if params: return key, params
	return "grid", {}

def rootParse(url, tklib, **params):
	master = params.pop("master", None)
	data = getXmlDom(url, **params)

	_return = data.attrib.pop("return", "list")
	if _return not in ["Tk", "Toplevel"]:
		return [elementParse(e, tklib, master) for e in listEtree(data)]
	elif _return == "Tk":
		root = getattr(tklib, _return)()
		for e in listEtree(data):
			elementParse(e, tklib, root)
		return root
	elif _return == "Toplevel":
		root = getattr(tklib, _return)(master, **data.attrib)
		for e in listEtree(data):
			elementParse(e, tklib, root) 
		return root

def elementParse(element, tklib, master=None):
	
	try:
		_class = getattr(tklib, element.tag)

	except AttributeError:
		warnings.warn('No %s attribute in %s librairy' % (element.tag, tklib), SyntaxWarning)

	else:
		obj = _class(master, name=element.attrib.pop("name", None))
		cnf = dict([k,element.attrib.pop(k)] for k in list(element.attrib.keys()) if str(k) in obj.keys())
		layout, params = stripLayout(element)

		obj.configure(cnf, **element.attrib)
		getattr(obj, layout)(**params)

		keepref = element.attrib.pop("pyobj", False)
		if keepref:
			setattr(obj.master, keepref, obj)

		# execute text
		tcl_text = "\n".join([l.strip() for l in element.text.split("\n") if l != ""] if element.text != None else [])
		if tcl_text != "": obj.tk.eval(tcl_text.format(**{"w":obj._w, "p":obj.master._w, "t":obj.winfo_toplevel()}))

		# parse sub elements
		for elem in listEtree(element): elementParse(elem, tklib, obj)

		# execute tail
		tcl_tail = "\n".join([l.strip() for l in element.tail.split("\n") if l != ""] if element.tail != None else [])
		if tcl_tail != "": obj.tk.eval(tcl_tail.format(**{"w":obj._w, "p":obj.master._w, "t":obj.winfo_toplevel()}))

		return obj

