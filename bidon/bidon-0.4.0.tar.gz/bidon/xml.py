from xml.sax import parse as sax_parse, parseString as sax_parse_string
from xml.sax.handler import ContentHandler
from xml.etree.ElementTree import Element


class ElementPuller(ContentHandler):
  """This is a SAX handler that builds ElementTree Elements for a subset of an XML document. It
  gives some of the niceties of ElementTree, but with a much lower memory footprint and a lot faster
  than pulldom.

  It works by having a tag or set of tags which will trigger tree building. Once a tag has been
  fully built it will be passed to the callback method. The file is read incrementally, and only the
  elements we're interested in are built out and returned.

  This is especially useful if your XML file is a collection of objects, and you can deal with them
  one at a time in isolation from each other. So you get single objects, but you can use the
  advanced API of ElementTree Elements on them.
  """
  def __init__(self, start_tag, callback):
    """Initialize the ElementPuller instance.

    start_tag can be either string or a set of strings.
    callback is a method that takes a single argument which is a fully constructed target tree.
    """
    self.start_tag = start_tag
    self._single_start = isinstance(start_tag, str)
    self.callback = callback
    self.stack = []

  @property
  def has_current(self):
    """Returns True if there is an element on the stack."""
    return bool(self.stack)

  @property
  def current(self):
    """Returns the element on the top of the stack."""
    return self.stack[-1]

  def parse(self, filename_or_stream):
    sax_parse(filename_or_stream, self)

  def parse_string(self, string):
    sax_parse_string(string, self)

  def is_start(self, tag):
    """Returns True if the given tag should trigger the start of building a tree."""
    return self._single_start and tag == self.start_tag or tag in self.start_tag

  def startElement(self, tag, attrib):
    """SAX startElement handler.

    If there is a tree being built, the element is popped onto the end of the current element's
    child list. If there is no tree being built, but the tag should start a new tree, a new tree
    is started. Otherwise the element is ignored.
    """
    if self.has_current or self.is_start(tag):
      elem = Element(tag, dict(attrib))
      if self.has_current:
        self.current.append(elem)
      self.stack.append(elem)

  def endElement(self, tag):
    """Pops the current element off the stack. If the stack is then empty, the element just popped
    is a tree root, and is therefore passed to callback.
    """
    if self.has_current:
      elem = self.stack.pop()
      if not self.has_current:
        self.callback(elem)

  def characters(self, content):
    """Appends character data to the current element."""
    if self.has_current and content:
      content = content.strip()
      if content:
        if self.current.text is None:
          self.current.text = content
        else:
          self.current.text += " " + content
