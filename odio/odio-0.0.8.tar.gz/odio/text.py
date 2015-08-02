import zipfile
import xml.dom.minidom
from six import iteritems, text_type
from xml.dom import Node


desc_style = {
    'Emphasis': 'Emphasis',
    'Heading 1': 'Heading_20_1',
    'Strong Emphasis': 'Strong_20_Emphasis',
    'Text Body': 'Text_20_body',
    'Title': 'Title'}

style_desc = dict((v, k) for k, v in iteritems(desc_style))


class OdioNode():
    def __init__(self, xml_name, default_attrs, xml_attrs, *nodes, **attrs):
        self.xml_name = xml_name
        self.default_attrs = default_attrs
        self.xml_attrs = xml_attrs
        self.nodes = list(nodes)
        self.attrs = attrs

        if default_attrs is not None:

            for k, v in iteritems(default_attrs):
                if k not in attrs:
                    attrs[k] = v

            for k, v in iteritems(attrs):
                if k == 'style':
                    self.xml_attrs['text:style-name'] = desc_style[v]
                elif k == 'outline_level':
                    self.xml_attrs['text:outline-level'] = str(v)

    def __repr__(self):
        args = []
        if self.default_attrs is None:
            args.append(str(self.xml_attrs))
            args.extend([repr(node) for node in self.nodes])
        else:
            args.extend([repr(node) for node in self.nodes])
            for k, v in iteritems(self.attrs):
                if k not in self.default_attrs or self.default_attrs[k] != v:
                    args.append(str(k) + '=' + str(v))
        return "odio." + self.__class__.__name__ + "(" + ', '.join(args) + ")"

    def __eq__(self, other):
        return isinstance(other, OdioNode) and \
            self.xml_name == other.xml_name and \
            self.nodes == other.nodes and self.xml_attrs == other.xml_attrs

    def _attach(self, doc, parent_elem):
        node_elem = doc.createElement(self.xml_name)
        parent_elem.appendChild(node_elem)
        for k, v in iteritems(self.xml_attrs):
            node_elem.setAttribute(k, v)
        for node in self.nodes:
            if isinstance(node, str):
                node_elem.appendChild(doc.createTextNode(node))
            else:
                node._attach(doc, node_elem)

    def append(self, *subnodes):
        self.nodes.extend(subnodes)


def _parse_node(node_dom):
    node_type = node_dom.nodeType
    if node_type == Node.ELEMENT_NODE:
        xml_name = node_dom.tagName
        xml_attrs = {}
        if node_dom.hasAttributes():
            attrs = node_dom.attributes
            for i in range(len(attrs)):
                attr = attrs.item(i)
                xml_attrs[attr.name] = attr.value
        nodes = []
        for subnode_dom in node_dom.childNodes:
            subnode = _parse_node(subnode_dom)
            if subnode is not None:
                nodes.append(subnode)
        for i in range(len(nodes)):
            if isinstance(nodes[i], text_type):
                if i == 0 and xml_name == 'text:p':
                    nodes[i] = nodes[i].lstrip()
                elif i > 0:
                    prev_subnode = nodes[i-1]
                    if isinstance(prev_subnode, OdioNode) and \
                            prev_subnode.xml_name == 'text:p':
                        nodes[i] = nodes[i].lstrip()

                if i == len(nodes) - 1:
                    nodes[i] = nodes[i].rstrip()
                elif i < len(nodes) - 1:
                    next_subnode = nodes[i+1]
                    if isinstance(next_subnode, OdioNode) and \
                            next_subnode.xml_name == 'text:p':
                        nodes[i] = nodes[i].rstrip()

        if 'text:style-name' in xml_attrs:
            attrs = {}
            for k, v in iteritems(xml_attrs):
                if k == 'text:style-name':
                    attrs['style'] = style_desc[v]
                elif k == 'text:outline-level':
                    attrs['outline_level'] = v
                else:
                    raise Exception(
                        "The XML attribute '" + k + "' isn't recognised.")

            node = style_classes[attrs['style']](*nodes, **attrs)
        else:
            if xml_name == 'text:p':
                node = P(xml_attrs, *nodes)
            elif xml_name == 'text:h':
                node = H(xml_attrs, *nodes)
            elif xml_name == 'text:span':
                node = Span(xml_attrs, *nodes)
            elif xml_name == 'office:text':
                node = Text(xml_attrs, *nodes)
            else:
                raise Exception("Node name " + xml_name + " not recognized.")
    elif node_type == Node.TEXT_NODE:
        fnode = node_dom.nodeValue
        snode = fnode.strip()
        if len(snode) == 0:
            return
        node = snode
        rnode = node.rstrip()
        if len(rnode) < len(fnode):
            node += ' '
        lnode = node.lstrip()
        if len(lnode) < len(fnode):
            node = ' ' + node
    else:
        raise Exception("Node type " + str(node_type) + " not recognized.")
    return node


class H(OdioNode):
    def __init__(self, xml_attrs, *nodes):
        OdioNode.__init__(self, 'text:h', None, xml_attrs, *nodes)


class P(OdioNode):
    def __init__(self, xml_attrs, *nodes):
        OdioNode.__init__(self, 'text:p', None, xml_attrs, *nodes)


class Span(OdioNode):
    def __init__(self, xml_attrs, *nodes):
        OdioNode.__init__(self, 'text:span', None, xml_attrs, *nodes)


class Text(OdioNode):
    def __init__(self, xml_attrs, *nodes):
        OdioNode.__init__(self, 'office:text', None, xml_attrs, *nodes)


class Title(OdioNode):
    def __init__(self, *nodes, **attrs):
        OdioNode.__init__(
            self, 'text:p', {'style': 'Title'}, {}, *nodes, **attrs)


class Heading1(OdioNode):
    def __init__(self, *nodes, **attrs):
        OdioNode.__init__(
            self, 'text:h', {'style': 'Heading 1', 'outline_level': '1'}, {},
            *nodes, **attrs)


class Paragraph(OdioNode):
    def __init__(self, *nodes, **attrs):
        OdioNode.__init__(
            self, 'text:p', {'style': 'Text Body'}, {}, *nodes, **attrs)


class Emphasis(OdioNode):
    def __init__(self, *nodes, **attrs):
        OdioNode.__init__(
            self, 'text:span', {'style': 'Emphasis'}, {}, *nodes, **attrs)


class StrongEmphasis(OdioNode):
    def __init__(self, *nodes, **attrs):
        OdioNode.__init__(
            self, 'text:span', {'style': 'Strong Emphasis'}, {}, *nodes,
            **attrs)


style_classes = {
    'Emphasis': Emphasis,
    'Heading 1': Heading1,
    'Strong Emphasis': StrongEmphasis,
    'Text Body': Paragraph,
    'Title': Title}


class TextWriter():
    def __init__(self, f, version='1.2'):
        self.f = f
        self.z = zipfile.ZipFile(f, 'w')
        self.z.writestr(
            'mimetype', 'application/vnd.oasis.opendocument.text')
        if version == '1.2':
            self.z.writestr(
                'META-INF/manifest.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest
    manifest:version="1.2"
    xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry
      manifest:full-path="/"
      manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry
      manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry
      manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry
      manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry
      manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
""")
            self.z.writestr(
                'meta.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    office:version="1.2">
  <office:meta>
      <meta:generator>Odio</meta:generator>
  </office:meta>
</office:document-meta>
""")

            self.z.writestr(
                'settings.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    office:version="1.2">
</office:document-settings>
""")

            self.z.writestr(
                'styles.xml', """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:css3t="http://www.w3.org/TR/css3-text/"
    office:version="1.2">
  <office:font-face-decls>
    <style:font-face
        style:name="FreeSans1" svg:font-family="FreeSans"
        style:font-family-generic="swiss"/>
    <style:font-face
        style:name="Liberation Serif" svg:font-family="'Liberation Serif'"
        style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face
        style:name="Liberation Sans" svg:font-family="'Liberation Sans'"
        style:font-family-generic="swiss" style:font-pitch="variable"/>
    <style:font-face
        style:name="Droid Sans Fallback"
        svg:font-family="'Droid Sans Fallback'"
        style:font-family-generic="system" style:font-pitch="variable"/>
    <style:font-face
        style:name="FreeSans" svg:font-family="FreeSans"
        style:font-family-generic="system" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:styles>
    <style:default-style style:family="graphic">
      <style:graphic-properties
          svg:stroke-color="#3465a4" draw:fill-color="#729fcf"
          fo:wrap-option="no-wrap" draw:shadow-offset-x="0.3cm"
          draw:shadow-offset-y="0.3cm"
          draw:start-line-spacing-horizontal="0.283cm"
          draw:start-line-spacing-vertical="0.283cm"
          draw:end-line-spacing-horizontal="0.283cm"
          draw:end-line-spacing-vertical="0.283cm"
          style:flow-with-text="false"/>
      <style:paragraph-properties
          style:text-autospace="ideograph-alpha" style:line-break="strict"
          style:writing-mode="lr-tb"
          style:font-independent-line-spacing="false">
        <style:tab-stops/>
      </style:paragraph-properties>
      <style:text-properties
          style:use-window-font-color="true" style:font-name="Liberation Serif"
          fo:font-size="12pt" fo:language="en" fo:country="GB"
          style:letter-kerning="true"
          style:font-name-asian="Droid Sans Fallback"
          style:font-size-asian="10.5pt" style:language-asian="zh"
          style:country-asian="CN" style:font-name-complex="FreeSans"
          style:font-size-complex="12pt" style:language-complex="hi"
          style:country-complex="IN"/>
    </style:default-style>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties
        fo:hyphenation-ladder-count="no-limit"
        style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging"
        style:line-break="strict" style:tab-stop-distance="1.251cm"
        style:writing-mode="page"/>
      <style:text-properties
          style:use-window-font-color="true" style:font-name="Liberation Serif"
          fo:font-size="12pt" fo:language="en" fo:country="GB"
          style:letter-kerning="true"
          style:font-name-asian="Droid Sans Fallback"
          style:font-size-asian="10.5pt" style:language-asian="zh"
          style:country-asian="CN"
          style:font-name-complex="FreeSans" style:font-size-complex="12pt"
          style:language-complex="hi" style:country-complex="IN"
          fo:hyphenate="false" fo:hyphenation-remain-char-count="2"
          fo:hyphenation-push-char-count="2"/>
    </style:default-style>
    <style:default-style style:family="table">
      <style:table-properties table:border-model="collapsing"/>
    </style:default-style>
    <style:default-style style:family="table-row">
      <style:table-row-properties fo:keep-together="auto"/>
    </style:default-style>
    <style:style
        style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style
        style:name="Heading" style:family="paragraph"
        style:parent-style-name="Standard" style:next-style-name="Text_20_body"
        style:class="text">
      <style:paragraph-properties
        fo:margin-top="0.423cm" fo:margin-bottom="0.212cm"
        fo:keep-with-next="always"/>
      <style:text-properties
        style:font-name="Liberation Sans" fo:font-family="'Liberation Sans'"
        style:font-family-generic="swiss" style:font-pitch="variable"
        fo:font-size="14pt" style:font-name-asian="Droid Sans Fallback"
        style:font-family-asian="'Droid Sans Fallback'"
        style:font-family-generic-asian="system"
        style:font-pitch-asian="variable" style:font-size-asian="14pt"
        style:font-name-complex="FreeSans" style:font-family-complex="FreeSans"
        style:font-family-generic-complex="system"
        style:font-pitch-complex="variable" style:font-size-complex="14pt"/>
    </style:style>
    <style:style
        style:name="Text_20_body" style:display-name="Text Body"
        style:family="paragraph" style:parent-style-name="Standard"
        style:class="text">
      <style:paragraph-properties
          fo:margin-top="0cm" fo:margin-bottom="0.247cm"
          fo:line-height="120%"/>
    </style:style>
    <style:style
        style:name="List" style:family="paragraph"
        style:parent-style-name="Text_20_body" style:class="list">
      <style:text-properties
          style:font-size-asian="12pt" style:font-name-complex="FreeSans1"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="swiss"/>
    </style:style>
    <style:style
        style:name="Caption" style:family="paragraph"
        style:parent-style-name="Standard" style:class="extra">
      <style:paragraph-properties
          fo:margin-top="0.212cm" fo:margin-bottom="0.212cm"
          text:number-lines="false"
          text:line-number="0"/>
      <style:text-properties
          fo:font-size="12pt" fo:font-style="italic"
          style:font-size-asian="12pt" style:font-style-asian="italic"
          style:font-name-complex="FreeSans1"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="swiss"
          style:font-size-complex="12pt" style:font-style-complex="italic"/>
    </style:style>
    <style:style
        style:name="Index" style:family="paragraph"
        style:parent-style-name="Standard" style:class="index">
      <style:paragraph-properties
          text:number-lines="false" text:line-number="0"/>
      <style:text-properties
        style:font-size-asian="12pt" style:font-name-complex="FreeSans1"
        style:font-family-complex="FreeSans"
        style:font-family-generic-complex="swiss"/>
    </style:style>
    <style:style
        style:name="Quotations" style:family="paragraph"
        style:parent-style-name="Standard" style:class="html">
      <style:paragraph-properties
          fo:margin-left="1cm" fo:margin-right="1cm" fo:margin-top="0cm"
          fo:margin-bottom="0.499cm" fo:text-indent="0cm"
          style:auto-text-indent="false"/>
    </style:style>
    <style:style
        style:name="Title" style:family="paragraph"
        style:parent-style-name="Heading" style:next-style-name="Text_20_body"
        style:class="chapter">
    <style:paragraph-properties
        fo:text-align="center" style:justify-single-word="false"/>
    <style:text-properties
        fo:font-size="28pt" fo:font-weight="bold" style:font-size-asian="28pt"
        style:font-weight-asian="bold" style:font-size-complex="28pt"
        style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Subtitle" style:family="paragraph"
        style:parent-style-name="Heading" style:next-style-name="Text_20_body"
        style:class="chapter">
      <style:paragraph-properties
        fo:margin-top="0.106cm" fo:margin-bottom="0.212cm"
        fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties
        fo:font-size="18pt" style:font-size-asian="18pt"
        style:font-size-complex="18pt"/>
    </style:style>
    <style:style
        style:name="Heading_20_1" style:display-name="Heading 1"
        style:family="paragraph" style:parent-style-name="Heading"
        style:next-style-name="Text_20_body" style:default-outline-level="1"
        style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.423cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
          fo:font-size="130%" fo:font-weight="bold"
          style:font-size-asian="130%" style:font-weight-asian="bold"
          style:font-size-complex="130%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Heading_20_2" style:display-name="Heading 2"
        style:family="paragraph" style:parent-style-name="Heading"
        style:next-style-name="Text_20_body" style:default-outline-level="2"
        style:class="text">
      <style:paragraph-properties
        fo:margin-top="0.353cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
        fo:font-size="115%" fo:font-weight="bold" style:font-size-asian="115%"
        style:font-weight-asian="bold" style:font-size-complex="115%"
        style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Heading_20_3" style:display-name="Heading 3"
        style:family="paragraph" style:parent-style-name="Heading"
        style:next-style-name="Text_20_body" style:default-outline-level="3"
        style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.247cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
          fo:font-size="101%" fo:font-weight="bold"
          style:font-size-asian="101%" style:font-weight-asian="bold"
          style:font-size-complex="101%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Strong_20_Emphasis" style:display-name="Strong Emphasis"
        style:family="text">
      <style:text-properties
          fo:font-weight="bold" style:font-weight-asian="bold"
          style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Emphasis" style:family="text">
      <style:text-properties
          fo:font-style="italic" style:font-style-asian="italic"
          style:font-style-complex="italic"/>
    </style:style>
    <text:outline-style style:name="Outline">
      <text:outline-level-style text:level="1" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="0.762cm" fo:text-indent="-0.762cm"
              fo:margin-left="0.762cm"/>
          </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style
          text:level="2" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="1.016cm" fo:text-indent="-1.016cm"
              fo:margin-left="1.016cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="3" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="1.27cm" fo:text-indent="-1.27cm"
              fo:margin-left="1.27cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="4" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
            text:label-followed-by="listtab"
            text:list-tab-stop-position="1.524cm" fo:text-indent="-1.524cm"
            fo:margin-left="1.524cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="5" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="1.778cm" fo:text-indent="-1.778cm"
              fo:margin-left="1.778cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="6" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="2.032cm" fo:text-indent="-2.032cm"
              fo:margin-left="2.032cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="7" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="2.286cm" fo:text-indent="-2.286cm"
              fo:margin-left="2.286cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="8" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="2.54cm" fo:text-indent="-2.54cm"
              fo:margin-left="2.54cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="9" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="2.794cm" fo:text-indent="-2.794cm"
              fo:margin-left="2.794cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="10" style:num-format="">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment
              text:label-followed-by="listtab"
              text:list-tab-stop-position="3.048cm" fo:text-indent="-3.048cm"
              fo:margin-left="3.048cm"/>
        </style:list-level-properties>
      </text:outline-level-style>
    </text:outline-style>
    <text:notes-configuration
        text:note-class="footnote" style:num-format="1" text:start-value="0"
        text:footnotes-position="page" text:start-numbering-at="document"/>
    <text:notes-configuration
        text:note-class="endnote" style:num-format="i" text:start-value="0"/>
    <text:linenumbering-configuration
        text:number-lines="false" text:offset="0.499cm" style:num-format="1"
        text:number-position="left" text:increment="5"/>
  </office:styles>
</office:document-styles>
""")
            self.doc = xml.dom.minidom.parseString(
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:css3t="http://www.w3.org/TR/css3-text/"
    office:version="1.2">
  <office:scripts/>
  <office:automatic-styles>
    <number:date-style style:name="date">
      <number:year number:style="long"/>
      <number:text>-</number:text>
      <number:month number:style="long"/>
      <number:text>-</number:text>
      <number:day number:style="long"/>
      <number:text> </number:text>
      <number:hours number:style="long"/>
      <number:text>:</number:text>
      <number:minutes number:style="long"/>
    </number:date-style>
    <style:style style:name="cell_date" style:family="table-cell"
      style:parent-style-name="Default" style:data-style-name="date"/>
  </office:automatic-styles>
  <office:body>
    <office:text>
    </office:text>
  </office:body>
</office:document-content>""")
        elif version == '1.1':
            self.z.writestr(
                'META-INF/manifest.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest
    xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
 <manifest:file-entry
     manifest:full-path="/"
     manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry
     manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry
     manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry
     manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry
     manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
""")
            self.z.writestr(
                'meta.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:grddl="http://www.w3.org/2003/g/data-view#"
    office:version="1.1">
  <office:meta>
    <meta:generator>Odio</meta:generator>
  </office:meta>
</office:document-meta>
""")

            self.z.writestr(
                'settings.xml',
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"/>
""")

            self.z.writestr(
                'styles.xml', """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:grddl="http://www.w3.org/2003/g/data-view#"
    xmlns:css3t="http://www.w3.org/TR/css3-text/"
    office:version="1.1">
  <office:font-face-decls>
    <style:font-face
      style:name="FreeSans1" svg:font-family="FreeSans"
      style:font-family-generic="swiss"/>
    <style:font-face
      style:name="Liberation Serif"
      svg:font-family="&apos;Liberation Serif&apos;"
      style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face
      style:name="Liberation Sans"
      svg:font-family="&apos;Liberation Sans&apos;"
      style:font-family-generic="swiss" style:font-pitch="variable"/>
    <style:font-face
      style:name="Droid Sans Fallback"
      svg:font-family="&apos;Droid Sans Fallback&apos;"
      style:font-family-generic="system" style:font-pitch="variable"/>
    <style:font-face
      style:name="FreeSans" svg:font-family="FreeSans"
      style:font-family-generic="system" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:styles>
    <style:default-style style:family="graphic">
      <style:graphic-properties
          svg:stroke-color="#3465a4" draw:fill-color="#729fcf"
          fo:wrap-option="no-wrap" draw:shadow-offset-x="0.3cm"
          draw:shadow-offset-y="0.3cm"
          draw:start-line-spacing-horizontal="0.283cm"
          draw:start-line-spacing-vertical="0.283cm"
          draw:end-line-spacing-horizontal="0.283cm"
          draw:end-line-spacing-vertical="0.283cm"
          style:flow-with-text="false"/>
      <style:paragraph-properties
          style:text-autospace="ideograph-alpha" style:line-break="strict"
          style:writing-mode="lr-tb"
          style:font-independent-line-spacing="false">
        <style:tab-stops/>
      </style:paragraph-properties>
      <style:text-properties
          style:use-window-font-color="true" style:font-name="Liberation Serif"
          fo:font-size="12pt" fo:language="en" fo:country="GB"
          style:letter-kerning="true"
          style:font-name-asian="Droid Sans Fallback"
          style:font-size-asian="10.5pt" style:language-asian="zh"
          style:country-asian="CN" style:font-name-complex="FreeSans"
          style:font-size-complex="12pt" style:language-complex="hi"
          style:country-complex="IN"/>
    </style:default-style>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties
          fo:hyphenation-ladder-count="no-limit"
          style:text-autospace="ideograph-alpha"
          style:punctuation-wrap="hanging" style:line-break="strict"
          style:tab-stop-distance="1.251cm" style:writing-mode="page"/>
      <style:text-properties
          style:use-window-font-color="true" style:font-name="Liberation Serif"
          fo:font-size="12pt" fo:language="en" fo:country="GB"
          style:letter-kerning="true"
          style:font-name-asian="Droid Sans Fallback"
          style:font-size-asian="10.5pt" style:language-asian="zh"
          style:country-asian="CN" style:font-name-complex="FreeSans"
          style:font-size-complex="12pt" style:language-complex="hi"
          style:country-complex="IN" fo:hyphenate="false"
          fo:hyphenation-remain-char-count="2"
          fo:hyphenation-push-char-count="2"/>
    </style:default-style>
    <style:default-style style:family="table">
      <style:table-properties table:border-model="collapsing"/>
    </style:default-style>
    <style:default-style style:family="table-row">
      <style:table-row-properties fo:keep-together="auto"/>
    </style:default-style>
    <style:style
        style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style
        style:name="Heading" style:family="paragraph"
        style:next-style-name="Text_20_body" style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.423cm" fo:margin-bottom="0.212cm"
          fo:keep-with-next="always"/>
      <style:text-properties
          style:font-name="Liberation Sans"
          fo:font-family="&apos;Liberation Sans&apos;"
          style:font-family-generic="swiss" style:font-pitch="variable"
          fo:font-size="14pt" style:font-name-asian="Droid Sans Fallback"
          style:font-family-asian="&apos;Droid Sans Fallback&apos;"
          style:font-family-generic-asian="system"
          style:font-pitch-asian="variable" style:font-size-asian="14pt"
          style:font-name-complex="FreeSans"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="system"
          style:font-pitch-complex="variable" style:font-size-complex="14pt"/>
    </style:style>
    <style:style
        style:name="Text_20_body" style:display-name="Text body"
        style:family="paragraph" style:class="text">
      <style:paragraph-properties
          fo:margin-top="0cm" fo:margin-bottom="0.247cm"
          fo:line-height="120%"/>
    </style:style>
    <style:style style:name="List" style:family="paragraph" style:class="list">
      <style:text-properties
          style:font-size-asian="12pt" style:font-name-complex="FreeSans1"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="swiss"/>
    </style:style>
    <style:style
        style:name="Caption" style:family="paragraph" style:class="extra">
      <style:paragraph-properties
          fo:margin-top="0.212cm" fo:margin-bottom="0.212cm"
          text:number-lines="false" text:line-number="0"/>
      <style:text-properties
          fo:font-size="12pt" fo:font-style="italic"
          style:font-size-asian="12pt" style:font-style-asian="italic"
          style:font-name-complex="FreeSans1"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="swiss"
          style:font-size-complex="12pt" style:font-style-complex="italic"/>
    </style:style>
    <style:style
        style:name="Index" style:family="paragraph" style:class="index">
      <style:paragraph-properties
          text:number-lines="false" text:line-number="0"/>
      <style:text-properties
          style:font-size-asian="12pt" style:font-name-complex="FreeSans1"
          style:font-family-complex="FreeSans"
          style:font-family-generic-complex="swiss"/>
    </style:style>
    <style:style
        style:name="Quotations" style:family="paragraph" style:class="html">
      <style:paragraph-properties
          fo:margin-left="1cm" fo:margin-right="1cm" fo:margin-top="0cm"
          fo:margin-bottom="0.499cm" fo:text-indent="0cm"
          style:auto-text-indent="false"/>
    </style:style>
    <style:style
        style:name="Title" style:family="paragraph"
        style:next-style-name="Text_20_body" style:class="chapter">
      <style:paragraph-properties
          fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties
          fo:font-size="28pt" fo:font-weight="bold"
          style:font-size-asian="28pt" style:font-weight-asian="bold"
          style:font-size-complex="28pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Subtitle" style:family="paragraph"
        style:next-style-name="Text_20_body" style:class="chapter">
      <style:paragraph-properties
          fo:margin-top="0.106cm" fo:margin-bottom="0.212cm"
          fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties
          fo:font-size="18pt" style:font-size-asian="18pt"
          style:font-size-complex="18pt"/>
    </style:style>
    <style:style
        style:name="Heading_20_1" style:display-name="Heading 1"
        style:family="paragraph" style:next-style-name="Text_20_body"
        style:default-outline-level="1" style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.423cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
          fo:font-size="130%" fo:font-weight="bold"
          style:font-size-asian="130%" style:font-weight-asian="bold"
          style:font-size-complex="130%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Heading_20_2" style:display-name="Heading 2"
        style:family="paragraph" style:next-style-name="Text_20_body"
        style:default-outline-level="2" style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.353cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
          fo:font-size="115%" fo:font-weight="bold"
          style:font-size-asian="115%" style:font-weight-asian="bold"
          style:font-size-complex="115%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Heading_20_3" style:display-name="Heading 3"
        style:family="paragraph" style:next-style-name="Text_20_body"
        style:default-outline-level="3" style:class="text">
      <style:paragraph-properties
          fo:margin-top="0.247cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties
          fo:font-size="101%" fo:font-weight="bold"
          style:font-size-asian="101%" style:font-weight-asian="bold"
          style:font-size-complex="101%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style
        style:name="Strong_20_Emphasis" style:display-name="Strong Emphasis"
        style:family="text">
      <style:text-properties
          fo:font-weight="bold" style:font-weight-asian="bold"
          style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Emphasis" style:family="text">
      <style:text-properties
          fo:font-style="italic" style:font-style-asian="italic"
          style:font-style-complex="italic"/>
    </style:style>
    <text:outline-style>
      <text:outline-level-style text:level="1" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="2" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="3" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="4" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="5" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="6" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="7" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="8" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="9" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
      <text:outline-level-style text:level="10" style:num-format="">
        <style:list-level-properties/>
      </text:outline-level-style>
    </text:outline-style>
    <text:notes-configuration
        text:note-class="footnote" style:num-format="1" text:start-value="0"
        text:footnotes-position="page" text:start-numbering-at="document"/>
    <text:notes-configuration
        text:note-class="endnote" style:num-format="i" text:start-value="0"/>
    <text:linenumbering-configuration
        text:number-lines="false" text:offset="0.499cm" style:num-format="1"
        text:number-position="left" text:increment="5"/>
  </office:styles>
  <office:automatic-styles>
  </office:automatic-styles>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="Mpm1"/>
  </office:master-styles>
</office:document-styles>
""")
            self.doc = xml.dom.minidom.parseString(
                """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:grddl="http://www.w3.org/2003/g/data-view#"
    xmlns:css3t="http://www.w3.org/TR/css3-text/"
    office:version="1.1">
  <office:scripts/>
  <office:font-face-decls>
    <style:font-face
        style:name="FreeSans1" svg:font-family="FreeSans"
        style:font-family-generic="swiss"/>
    <style:font-face
        style:name="Liberation Serif"
        svg:font-family="&apos;Liberation Serif&apos;"
        style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face
        style:name="Liberation Sans"
        svg:font-family="&apos;Liberation Sans&apos;"
        style:font-family-generic="swiss" style:font-pitch="variable"/>
    <style:font-face
        style:name="Droid Sans Fallback"
        svg:font-family="&apos;Droid Sans Fallback&apos;"
        style:font-family-generic="system" style:font-pitch="variable"/>
    <style:font-face
        style:name="FreeSans" svg:font-family="FreeSans"
        style:font-family-generic="system" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:automatic-styles/>
  <office:body>
    <office:text>
    </office:text>
  </office:body>
</office:document-content>""")

        self.text_elem = self.doc.getElementsByTagName(
            'office:text')[0]
        self.text = Text({})

    def close(self):
        for node in self.text.nodes:
            node._attach(self.doc, self.text_elem)

        self.z.writestr('content.xml', self.doc.toprettyxml(encoding='utf-8'))
        self.z.close()
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class TextReader():
    def __init__(self, f):
        with zipfile.ZipFile(f, 'r') as z:
            content = z.read('content.xml')
        f.close()
        dom = xml.dom.minidom.parseString(content)
        text_elem = dom.getElementsByTagName('office:text')[0]
        self.text = _parse_node(text_elem)
