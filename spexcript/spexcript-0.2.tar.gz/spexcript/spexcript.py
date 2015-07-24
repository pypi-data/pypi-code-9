#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created in 2013

@author: Koos Zevenhoven
"""
from __future__ import unicode_literals, print_function, division
import re
import six
#TODO: more automatic generation of this stuff (eliminate redundant info)
#The main issue is how to deal with alternate control keys ("<" and "\\")

section_key_char = "#"

container_keys = {"#": "Section",
                  "##": "Section",
                  "###": "Section",
                  "####": "Section",
                  "<": "Block",
                  "\\": "Block",
                  "+": "Block", #temporarily also a block...
                  "%": "Character",
                  "": "Text",
                  "*": "Effect",
                  "$": "Music", 
                  "$$": "Song",
                  "---": "Intermission",
                  None: "Spexcript"}

title_format = { "Section": ["line"],
                 "Character": ["chain", "line"],
                 "Text": [],
                 "Block": ["chain"],
                 "Music": ["chain"],
                 "Song": ["chain"],
                 "Effect": [],
                 "Intermission": [] } 

container_hierarchy = [["#"], ["##"], ["###"], ["####"], 
                       ["---", "+", "$", "$$", "%", "\\", "<"]]
# by default, anything can contain "Text"
container_test_order = list(reversed([c for cl in container_hierarchy for c in cl]))

# extract hierarchy into dictionaries
can_contain = dict()
cant_contain = dict()
for i in range(len(container_hierarchy) - 1):
    # each container can cantain anything that comes after the current one in the hierarchy
    can = [c for cl in container_hierarchy[i+1:] for c in cl]
    cant = [c for cl in container_hierarchy[0:i+1] for c in cl]
    for key in container_hierarchy[i]:
        can_contain[key] = can
        cant_contain[key] = cant
del can, cant, key, i

def split_key(titleline):
    """Identify and separate container key of the given titleline.

    Return a tuple (key, rest_of_line), where key contains the spextex
    container key and rest_of_line contains the rest of the title line.

    If no key is recognized, return "", possibly meaning a Text container.
    """
    #TODO : SYNTAX REFINEMENT: SHOULD WE ALLOW WHITESPACE BEFORE KEY (now yes)
    for key in container_test_order:
        if titleline.lstrip().startswith(key):
            # NOTE: lstrip strips the characters in any combination, so
            # the first whitespace character should end stripping.
            return (key, titleline.lstrip().lstrip(key))
    return "", titleline


def filewrap(inputfile, first_line_number = 1, coding = "utf8"):
    """Wrap a file-like object in a "filewrapper" generator.

    Return a generator that, line by line, yields the contents of the
    file-like tuples (line_number, line).  An important feature of this wrapper
    is that the last yielded line can be "pushed back" by invoking the the send
    method of the generator: if the argument is non-None but not unicode, this
    will undo the previous next(), and if unicode, the contents thereof will be
    yielded next time. If the file object is not positioned at the first
    line of the spexdown file, the number of the first readable line should
    be given as an argument.

    Note: The data read is decoded into unicode objects assuming the encoding
    optionally given.

    Arguments:
        inputfile -- file-like object to be wrapped
        first_line_number -- number of the next line in inputfile (optional)
        coding -- the character encoding the file has been saved in
    """
    def handle_curly_comments(line, level):
        #handle most typical cases first for speed
        if not "{" in line and not "}" in line:
            if level > 0:
                return None, level
            return line, 0
        
        visible = ""
        for c in line:
            if c == "{":
                level += 1
                continue
            if c == "}":
                level -= 1
                if level < 0:
                    level = 0
                continue
            if level == 0:
                visible += c
        return (visible, level) if len(visible) > 0 else (None, level)
            
                
    line_number = first_line_number
    curly_level = 0
    with inputfile:
        for line in inputfile:
            if isinstance(line, six.binary_type):
                line = line.decode(coding)
            line, curly_level = handle_curly_comments(line, curly_level)
            if line == None:
                continue
            push_back = yield (line_number, line)
            while push_back != None:
                if isinstance(push_back, six.text_type):
                    line = push_back
                yield line_number # send returns only the line number
                push_back = yield (line_number,line) # re-yield the line on following next

            line_number += 1


def load_spexcript(inputfile, first_line_number = 1):
    """Parse a Spexcript object from file-like spexcript source.

    Technically, inputfile is wrapped using filewrap() and passed on to
    the constructor of Spexcript.

    Arguments:
        inputfile -- file-like object to parse from
        first_line_number -- number of the next line in inputfile (if not 1)
    """
    filewrapper = filewrap(inputfile, first_line_number)
    from layout import Spexcript
    return Spexcript(filewrapper)

def multiple_replacer(replace_dict):
    #TODO need to properly handle delimiter after character name or abbr.
    replace_items = sorted(replace_dict.items(), key = lambda x: -len(x[0]))
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join(
        re.escape(k) for k, v in replace_items), re.M
    )
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, replace_dict):
    return multiple_replacer(replace_dict)(string)

def parse_filewrapper(filewrapper, parent = None):
    """Return generator to parse Containers from spexdown filewrapper source.

    Return generator object that parses a sequence of Container objects from
    spexdown code. Subcontainers will be parsed recursively. The iteration
    will stop when a container is encountered that cannot be contained by the
    parent. If the parent is None (default), parsing continues to the end of
    the file.

    One should make sure the file line numbering in the filewrapper is correct,
    that is, counted from the beginning of the _whole_ spexdown source.
    Incorrect line numbering does not prevent parsing, but can harm subsequent
    attempts to reparse only a portion of a spexdown file.

    Arguments:
        inputfile -- filewrapper object to parse from (see filewrap())
        parent -- parent object (instance of a subclass of Container)
    """

    # contents of Text are simply paragraphs -> handle separately
    # may need to move this functionality to Container.parse to allow
    # commands/containers inside paragraphs
    if parent != None and container_keys[parent.key] == "Text":
        replacer = multiple_replacer(
            {'@' + c: '@' + char 
                for c, char in parent.get_name_dict().items()}
        )
        
        for par in get_paragraphs(filewrapper):
            par = replacer(par)            
            yield par
        return

    # assume first container is Text (will be empty if not)
    yield Container.parse(filewrapper, parent, "")

    for number, line in filewrapper:
        key = split_key(line)[0]
        filewrapper.send(True) # pushes back the first line
        if parent != None and not parent.can_contain(key):
            return # the container found cannot be contained by parent
        yield Container.parse(filewrapper, parent, key)

def count_leading(data, char):
    """Count number of character (char) in the beginning of string (data) """
    for i in range(len(data)):
        if data[i] != char:
            return i
    return len(data)

def get_section_priority(raw):
    """Get spexdown section priority for raw spexdown code (number of "#"s)"""
    return count_leading(raw.lstrip(), section_key_char)

def get_paragraphs(filewrapper):
    """Read paragraphs of text from a file wrapper, until next container."""
    par = ''

    for num, line in filewrapper:
        key, line = split_key(line)
        if  key != "":
            filewrapper.send(True) # push line back (part of next Container)
            break #found container that cannot be contained

        if line.strip() == '':
            if par != '':
                yield par
                par = ''
        else:
            par += line.strip() + ' '

    if par != '':
        yield par
        
def parse_chain(data):
    #TODO implement full chain
    
    try:
        chain, rest = data.split(None, 1)
    except ValueError:
        #split did not return two parts 
        chain = data.strip()
        rest = ""
    
    def split_chain(data, delim):
        return (d for dat in data for d in dat.split(delim) )
    
    data = [chain]
    delims = ["&", "(", ")", ","]    
    for d in delims:
        data = split_chain(data, d)
    return list(filter(lambda x: x != '', data)), rest
    

class Container(object):
    """ Base class for all elements of a spexdown source. In the source, a
    container typically starts with a key consisting of one or more characters.
    This key determines the type of container. The container called "Text" is
    an exception in the sense that it does not begin with a key: it just
    contains one or more paragraphs of text.

    The key is immediately followed by the "title", which may be anything from
    one char to a full line (the rest of the key line). The "title", contains
    information specific to the container type, and is in turn followed by the
    body of the container: one or more other containers. By default, the
    body/contents of any container begin with a Text container. The body of a
    container end at the beginning of another container, which the first
    container is not able to contain (right before the key).

    Each container has a parent container, i.e., the container that contains
    it. The most outer container has parent = None, being the ancestor of all
    containers in this file/script. A Container object has a weak reference to
    its parent (i.e. no cyclic reference for the garbege collector)

    Containers roughly map to elements in the output, although all container
    types do not necessarily need to produce an output. Containers may also not
    appear in the same order as defined in the source, although most do.

    This base class aims to provide most of the generic functionality required
    for parsing containers etc., leaving only small details to subclasses.
    """

    @staticmethod
    def parse(filewrapper, parent = None, key = None):
        """Parse Container and contents from spexdown.
    
        Read in a full spexdown container, recursing to subcontainers.
        The container will be assumed to end if the last line from filewrapper
        has been read or if a container is encountered that cannot be contained in
        this container.
    
        One should make sure the file line numbering in the filewrapper is correct,
        that is, counted from the beginning of the _whole_ spexdown source.
        Incorrect line numbering does not prevent parsing, but can harm subsequent
        attempts to reparse only a portion of a spexdown file.
    
        If known, the spexdown key that determines the container type can be given
        as an argument to save a little bit of unnecessary work. If not given
        (key = None), it will be determined from the given data. If key = "", or
        the data does not start with a known key, a Text container is assumed.
    
        Returns:
            instance of a subclass of Container
    
        Arguments:
            filewrapper -- a generator to read from (see filewrap())
            parent -- the parent Container that will contain this object
            key -- string/character determining container type (default: read from data)
        """
        import layout
        
        if key == None:
            #determine class from data
            key = split_key(filewrapper.next())
            filewrapper.send(True) # Push back the whole line
    
        class_ = getattr(layout, container_keys[key])
    
        return class_(filewrapper, parent, key)
        
        
    def __init__(self, filewrapper, parent, key = None):
        """ Generic constructor for spexdown containers

        This constructor is in charge of parsing a spexdown container. It
        delegates most of the work to other functions, and, as little as
        possible, to subclasses. Typically, subclasses should not have their own
        constructors, but reimplement some methods instead.

        The given filewrapper should begin at the first line on the container,
        including the key character or string.

        Arguments:
            filewrapper -- filewrapper object (see filewrap())
            parent -- instance of sublcass of Container (or None, if top-level)
        """
        from weakref import proxy
        self.parent = proxy(parent) if parent != None else None

        linenum, title_line = next(filewrapper)
        self.key,rest = split_key(title_line)
                
        if key != None:
            self.key = key
        #TODO: assert key is compatible with this container class
        
        self._parse_title(rest, filewrapper)
        self._parse_contents(filewrapper)

    def _parse_title(self, rest, filewrapper):
        """Get title data and push remaining data back to wrapper."""
        
        form = title_format[self.__class__.__name__]

        title_data = []
        for elem in form:
            if elem == "chain":
                #TODO: proper chain reader
                if len(rest) < 1 or rest[0].isspace():
                    data = [""]
                    rest = rest.lstrip()
                else:
                    data, rest = parse_chain(rest)
                        
                title_data.append(data)
            elif elem == "line":
                title_data.append(rest.strip())
                rest = None
            else:
                raise RuntimeError("Unknown title format type (" + elem +")")

        if rest != None and self.key != "":
            filewrapper.send(rest) # push the rest back -- belongs to contents
        if self.key == "":
            filewrapper.send(True) # push the whole line back

        self._set_title_data(title_data)

    def _set_title_data(self, title_data):
        """Sets title data to self
        
        This is here so that subclasses can override.
        TODO: automatically save data in dictionary without asking subclass.
        """
        self.title = title_data
        
    def _parse_contents(self, filewrapper):
        """Parse contents from filewrapper (call from constructor) to self."""
        self._contents = []    
        for cont in parse_filewrapper(filewrapper, self):
            self._add_container(cont)

    def _add_container(self, cont): 
        #from layout import Character
        #if isinstance(cont, Character):
        #    pass #TODO: delegate to parent or catch it if no parent, or other reason
        #else:
        self._contents.append(cont)

    def can_contain(self, key):
        if self.key == None:
            return True #Spexcript can contain anything
        if self.key in can_contain:
            return key in can_contain[self.key]
        else:
            return False

    def generate_text(self):
        raise NotImplementedError("Text generation not implemented")

    def get_characters(self):
        raw_chars = [cc for c in self.get_contents() 
                            for cc in c.get_characters()]

        chars = []
        for c in raw_chars:
            if not c in chars:
                chars.append(c)
        return chars
        
    def get_characters_and_more(self):
        from itertools import dropwhile
        raw_list = [cc for c in self.get_contents() 
                            for cc in c.get_characters_and_more()]
        
        processed = []
        set_of_chars = set()
        set_of_conts = set()
        for cont, chars in raw_list:
            if chars == []:
                #no characters involved
                if not cont in set_of_conts:
                    set_of_conts.add(cont)
                    processed.append(([cont], ""))
                continue
            
            for ch in chars:
                if not ch in set_of_chars:
                    set_of_chars.add(ch)
                    #set_of_conts.add(cont)
                    processed.append(([cont], ch))
                else:
                    contlist = next(dropwhile(lambda x: x[1] != ch, processed))[0]
                    if not cont in contlist:
                        contlist.append(cont)
                
        return processed

    def get_contents(self):
        return list(self._contents)

    def get_name_dict(self):
        from layout import Character
        if self.parent == None:
            return dict()
        
        def get_from_parent():
            for c in self.parent._contents:
                if c == self:
                    return
                if isinstance(c, Character):
                    for a in c.abbreviations:
                        yield (a, c.display_name)
        
        names = dict(get_from_parent())
        names.update(self.parent.get_name_dict())
        
        return names
    
    def contains_sections(self):
        from layout import Section
        return any(isinstance(c, Section) for c in self._contents)
        
    def get_level_inner(self):
        #TODO should this be w.r.t. most inner level of whole spexcript?
        from layout import Section
        if not isinstance(self, Section):
            return 0
        
        return 1 + max(c.get_level_inner() for c in self._contents)
                
    def get_raw_numbering(self):
        if self.parent == None:
            return []
        return (self.parent.get_raw_numbering() +
                [self.parent._contents.index(self)])
     
    def get_section_numbering(self):
        from layout import Section
        if self.parent == None:
            return []
        i = 0
        
        for c in self.parent._contents:
            if isinstance(c, Section):
                i += 1
            if c == self:
                return (self.parent.get_section_numbering() + [i])
        
        assert False # should never reach here (parent should contain self)
    
    def __repr__(self):
        return self.generate_text()


def read_spex_file(filename):
    with open(filename, "r", encoding = 'utf8') as f:
        spexcript = load_spexcript(f)
    return spexcript # the spex itself

if __name__ == "__main__":
    import sys
    spex = read_spex_file(sys.argv[1])
    from language import Finnish
    from latex import Spextex
    spextex = Spextex(Finnish)
    spex.generate_front_page(spextex)
    spex.generate_characters(spextex)
    spex.generate_listing(spextex)
    spex.generate_script(spextex)
    tex = spextex.final_result()
    import latex
    latex.pdflatex(tex)
    latex.show()    
    
#    txt = spex.generate_text()
#   with open("output.txt","w") as f:
#       f.write(txt.encode("utf8"))
