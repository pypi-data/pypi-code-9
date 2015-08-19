#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path
import StringIO
import lxml.etree as ET

import dhtmlparser
from marcxml_parser import MARCXMLRecord


# Variables ===================================================================
XML_TEMPLATE = """<root>
<collection xmlns="http://www.loc.gov/MARC21/slim"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.loc.gov/MARC21/slim \
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
$CONTENT
</collection>
</root>
"""


# Functions & objects =========================================================
def _oai_to_xml(marc_oai):  # TODO: move this to MARC XML parser?
    """
    Convert OAI to MARC XML.

    Args:
        marc_oai (str): String with either OAI or MARC XML.

    Returns:
        str: String with MARC XML.
    """
    record = MARCXMLRecord(marc_oai)
    record.oai_marc = False

    return record.to_XML()


def _add_namespace(marc_xml):
    """
    Add proper XML namespace to the `marc_xml` record.

    Args:
        marc_xml (str): String representation of the XML record.

    Returns:
        str: XML with namespace.
    """
    dom = marc_xml

    if isinstance(dom, basestring):
        dom = dhtmlparser.parseString(marc_xml)

    root = dom.find("root")
    if root:
        root[0].params = {}

    for record in dom.find("record"):
        record.params = {}

    collections = dom.find("collection")
    if not collections:
        record = dom.find("record")[0]
        return XML_TEMPLATE.replace("$CONTENT", str(record))

    for col in collections:
        col.params["xmlns"] = "http://www.loc.gov/MARC21/slim"
        col.params["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        col.params["xsi:schemaLocation"] = "http://www.loc.gov/MARC21/slim " + \
                   "http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"

    return str(dom)


def _read_content_or_path(content_or_path):
    """
    If `content_or_path` contains ``\\n``, return it. Else assume, that it is
    path and read file at that path.

    Args:
        content_or_path (str): Content or path to the file.

    Returns:
        str: Content.

    Raises:
        IOError: whhen the file is not found.
    """
    if "\n" in content_or_path.strip():
        return content_or_path

    if not os.path.exists(content_or_path):
        raise IOError("File '%s' doesn't exists!" % content_or_path)

    with open(content_or_path) as f:
        return f.read()


def _read_marcxml(xml):
    """
    Read MARC XML or OAI file, convert, add namespace and return XML in
    required format with all necessities.

    Args:
        xml (str): Filename or XML string. Don't use ``\\n`` in case of
                   filename.

    Returns:
        obj: Required XML parsed with ``lxml.etree``.
    """
    # read file, if `xml` is valid file path
    marc_xml = _read_content_or_path(xml)


    # process input file - convert it from possible OAI to MARC XML and add
    # required XML namespaces
    marc_xml = _oai_to_xml(marc_xml)
    marc_xml = _add_namespace(marc_xml)

    file_obj = StringIO.StringIO(marc_xml)

    return ET.parse(file_obj)


def _read_template(template):
    """
    Read XSLT template.

    Args:
        template (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.

    Returns:
        obj: Required XML parsed with ``lxml.etree``.
    """
    template = _read_content_or_path(template)
    file_obj = StringIO.StringIO(template)

    return ET.parse(file_obj)


def xslt_transformation(xml, template):
    """
    Transform `xml` using XSLT `template`.

    Args:
        xml (str): Filename or XML string. Don't use ``\\n`` in case of
                   filename.
        template (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.

    Returns:
        str: Transformed `xml` as string.
    """
    transformer = ET.XSLT(
        _read_template(template)
    )
    newdom = transformer(
        _read_marcxml(xml)
    )

    return ET.tostring(newdom, pretty_print=True, encoding="utf-8")
