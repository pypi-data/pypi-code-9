# -*- coding: utf-8 -*-
"""
Created on Sat Feb 02 16:44:12 2013

@author: Koos Zevenhoven
"""
from __future__ import unicode_literals, print_function, division

from spexcript import Container
from abc import ABCMeta, abstractmethod
import text

class Layout(object):
    """Abstract class for a layout in which content is to be formatted.
    
    Subclasses of this may represent, for example, a character listing.
    The instances are in charge of the output generation process, but it
    passes itself to the displayed container objects so that they can check
    the Layout instance for details about the output layout.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def container_output(self, container, encoder):
        """Process a Container for output."""
        pass
        

class Text(Container):
    """A container with paragraphs of text."""
    # TODO: enable name tags and other features in text
    
    def get_characters(self):
        return []
    
    def get_characters_and_more(self):
        return []
        
    def generate_text(self, width=79, indent=0):
        lines = text.wrapped_lines(self._contents, width=width-indent)
        return (text.line_end + " " * indent).join(lines)
    
    def generate_dump(self, target):
        target.paragraphs(self._contents)
    
    def generate_characters(self, target):
        pass
    
    def generate_script(self, target):
        pass #Text objects are usually handled by the parent
        
class Character(Container):
    """A container decribing a character/person in a script"""
    
    def _set_title_data(self, title_data):
        self.display_name = title_data[0][0]
        self.abbreviations = title_data[0][1:]
        print (self.display_name, self.abbreviations)
        self.full_name = title_data[1]
        
    def generate_text(self, width=79):
        txt = self.full_name + text.line_end + \
            self._contents[0].generate_text(width=width, 
                                            indent=text.char_descr_indent)
        return txt
        
    def get_characters(self):
        return [self.display_name]
    
    def get_characters_and_more(self):
        return [(self.__class__.__name__, [self.display_name])]
        
    def generate_dump(self, target):
        target.character(self.display_name, 
                         self.full_name, 
                         self._contents[0]._contents)

    def generate_characters(self, target):
        self.generate_dump(target)
    
    def generate_script(self, target):
        pass
        
class Block(Container):
    def _set_title_data(self, title_data):
        labels = title_data[0]
        names = self.parent.get_name_dict()
        self.characters = [names.get(l,l) for l in labels if l != ""]
        #TODO: save references to Character objects instead?

    def get_characters(self):
        return list(self.characters)

    def get_characters_and_more(self):
        return [(self.__class__.__name__, self.characters)]

    
    def generate_text(self, width=79, labelwidth=10):
        label = "&".join(self.characters)
        
        labelwidth = max([len(label) + 2,labelwidth])
        labelwidth = min(labelwidth, width/2)
        
        label = label + ":"
        label = label.ljust(labelwidth)
        label = label[0:labelwidth]
    
        if self.characters == []:
            labelwidth = 0
            label = ""
               
        body = self._contents[0].generate_text(width, indent = labelwidth)
        
        return label + body
    
    def generate_dump(self, target):
        paragraphs = self._contents[0]._contents
        if len(paragraphs) > 0:
            #empty blocks (len = 0) are only for tagging people, no output
            target.block(self.characters, paragraphs)
    
    def generate_characters(self, target):
        pass
    
    def generate_script(self, target):
        self.generate_dump(target)
        
class Music(Block):
    def generate_dump(self, target):
        target.music(self.characters, 
                     self._contents[0]._contents, style = "music")

class Song(Block):
    def generate_dump(self, target):
        target.music(self.characters, 
                     self._contents[0]._contents, style = "song")
     

class Intermission(Container):
    def generate_dump(self, target):
        target.intermission()
    
    def generate_characters(self, target):
        pass
    
    def generate_script(self, target):
        self.generate_dump(target)
    
    def generate_listing(self, target):
        self.generate_dump(target)
    
    def get_characters_and_more(self):
        return []

        
class Section(Container):
    MAX_LEVEL = 3 

    def _set_title_data(self, title_data):
        self.title = title_data[0]
             
    def generate_text(self, width = 79):
        try:
            txt = self.title + "\n"
        except AttributeError:
            txt = ""
        
        if not self.contains_sections():
            ctxt = (c.generate_text(width = width) for c in self._contents)                   
            txt += text.line_end.join(ctxt)
        else:
            #def_sep = txt_line_end*(1+Section.MAX_LEVEL-self.level)
            def_sep = text.line_end * 3
            sep = ""
            wasblock = False
            
            for c in self._contents:
                
                isblock = isinstance(c, Block)
                if isblock and wasblock:
                    sep = text.line_end
                
                txt += sep + c.generate_text(width=width)
                
                sep = def_sep
                wasblock = isblock
        
        return txt
    
    def _generate_title(self, target, listing = False):
        numbering = self.get_section_numbering()
        
        pars = self._contents[0]._contents if listing else []
        if self.contains_sections():
            if self.get_level_inner() <= 2:
                target.act(numbering[-1], self.title, listing = listing)
        else:
            #TODO what if scene not inside act
            target.scene(numbering[-2], numbering[-1], self.title,
                         people = self.get_characters_and_more(),
                         description_pars = pars,
                         listing = listing)
   
    def generate_dump(self, target):
        self._generate_title(target)        
        
        for c in self._contents[1:]:
            c.generate_dump(target)
        
        if not self.contains_sections():
            target.scene_end()

    def generate_script(self, target, title = False):
        if title:
            target.script_title()
        
        self._generate_title(target)
        
        for c in self._contents[1:]:
            c.generate_script(target)
        
        if not self.contains_sections():
            target.scene_end()
    
    def generate_listing(self, target, title = False):
        if title:
            target.listing_title()
        
        self._generate_title(target, listing = True)
        
        for c in self._contents[1:]:
            if isinstance(c, Section) or isinstance(c, Intermission):
                c.generate_listing(target)
                
    
    def generate_characters(self, target, title = False):
        if title:
            target.characters_title()
        for c in self._contents:
            c.generate_characters(target)
            
    def generate_front_page(self, target):
        target.front_page(self.title)
    
    
class Spexcript(Section):
    """The contents (including linked content) of a spexcript source."""
    
    def __init__(self, filewrapper):
        self.key, self.parent = None, None
        self._parse_contents(filewrapper)
    
    def generate_dump(self, target):
        for c in self._contents:
            c.generate_dump(target)
            
    def generate_characters(self, target):
        Section.generate_characters(self, target, title = True)
        
    def generate_script(self, target):
        Section.generate_script(self, target, title = True)
    
    def generate_listing(self, target):
        Section.generate_listing(self, target, title = True)
    
    def generate_front_page(self, target):
        for c in self._contents:
            if isinstance(c, Section):
                c.generate_front_page(target)


#remove characterlist? should be a layout instead? (no, not layout)
class CharacterList(Container):
    """A container that maintains an ordered set of characters"""
    
    def __init__(self, characters = []):
        self._contents = characters
    
    def get_name_dict(self):
        d = dict((a,c.display_name) for c in self.characters for a in c.abbreviations)
        return d
    
    def generate_text(self, width=79):
        text.char_separator = text.line_end*2
        txt = "HENKILÖT" + text.line_end*2        
        txt += text.char_separator.join([c.generate_text(width=width) for c in self.characters])
    
    def get_contents(self):
        return self.characters
        

#Seems not needed
class Spex(Section):
    def get_name_dict(self):
        return self.charlist.get_name_dict()
    def __init__(self, raw_source, parent = None):
        self.charlist = CharacterList()        
        Section.__init__(self, raw_source, parent)
        