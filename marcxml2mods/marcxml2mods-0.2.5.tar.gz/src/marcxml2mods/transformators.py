#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path

import dhtmlparser
from marcxml_parser import MARCXMLRecord

import mods_postprocessor
from xslt_transformer import xslt_transformation
from xslt_transformer import _read_content_or_path


# Functions & classes =========================================================
def _absolute_template_path(fn):
    """
    Return absolute path for filename from local ``xslt/`` directory.

    Args:
        fn (str): Filename. ``MARC21slim2MODS3-4-NDK.xsl`` for example.

    Returns:
        str: Absolute path to `fn` in ``xslt`` dicretory..
    """
    return os.path.join(os.path.dirname(__file__), "xslt", fn)


def _apply_postprocessing(marc_xml, xml, func, uuid, url):
    """
    Apply `func` to all ``<mods:mods>`` tags from `xml`. Insert UUID.

    Args:
        marc_xml (str): Original Aleph record.
        xml (str): XML which will be postprocessed.
        func (fn): Function, which will be used for postprocessing.
        uuid (str): UUID, which will be inserted to `xml`.
        url (str): URL of the publication (public or not).

    Returns:
        list: List of string with postprocessed XML.
    """
    dom = dhtmlparser.parseString(xml)

    return [
        func(marc_xml, mods_tag, uuid, cnt, url)
        for cnt, mods_tag in enumerate(dom.find("mods:mods"))
    ]


def transform_to_mods_mono(marc_xml, uuid, url):
    """
    Convert `marc_xml` to MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.
        url (str): URL of the publication (public or not).

    Returns:
        list: Collection of transformed xml strings.
    """
    marc_xml = _read_content_or_path(marc_xml)

    transformed = xslt_transformation(
        marc_xml,
        _absolute_template_path("MARC21slim2MODS3-4-NDK.xsl")
    )

    return _apply_postprocessing(
        marc_xml=marc_xml,
        xml=transformed,
        func=mods_postprocessor.postprocess_monograph,
        uuid=uuid,
        url=url,
    )


def transform_to_mods_multimono(marc_xml, uuid, url):
    """
    Convert `marc_xml` to multimonograph MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.
        url (str): URL of the publication (public or not).

    Returns:
        list: Collection of transformed xml strings.
    """
    marc_xml = _read_content_or_path(marc_xml)

    transformed = xslt_transformation(
        marc_xml,
        _absolute_template_path("MARC21toMultiMonographTitle.xsl")
    )

    return _apply_postprocessing(
        marc_xml=marc_xml,
        xml=transformed,
        func=mods_postprocessor.postprocess_multi_mono,
        uuid=uuid,
        url=url,
    )


def transform_to_mods_periodical(marc_xml, uuid, url):
    """
    Convert `marc_xml` to periodical MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.
        url (str): URL of the publication (public or not).

    Returns:
        list: Collection of transformed xml strings.
    """
    marc_xml = _read_content_or_path(marc_xml)

    transformed = xslt_transformation(
        marc_xml,
        _absolute_template_path("MARC21toPeriodicalTitle.xsl")
    )

    return _apply_postprocessing(
        marc_xml=marc_xml,
        xml=transformed,
        func=mods_postprocessor.postprocess_periodical,
        uuid=uuid,
        url=url,
    )


def type_decisioner(marc_xml, mono_callback, multimono_callback,
                    periodical_callback):
    """
    Detect type of the `marc_xml`. Call proper callback.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        mono_callback (fn reference): Callback in case of monographic
                      publications.
        multimono_callback (fn reference): Callback used in case of
                           multi-monographic publications.
        periodical_callback (fn reference): Callback used in case of periodical
                            publications.

    Returns:
        obj: Content returned by the callback.

    Raises:
        ValueError: In case that type couldn't be detected.
    """
    marc_xml = _read_content_or_path(marc_xml)
    record = MARCXMLRecord(marc_xml)

    if record.is_monographic or record.is_single_unit:
        return mono_callback()
    elif record.is_multi_mono:
        return multimono_callback()
    elif record.is_continuing:
        return periodical_callback()

    raise ValueError("Can't identify type of the `marc_xml`!")


def marcxml2mods(marc_xml, uuid, url):
    """
    Convert `marc_xml` to MODS. Decide type of the record and what template to
    use (monograph, multi-monograph, periodical).

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.
        url (str): URL of the publication (public or not).

    Returns:
        list: Collection of transformed xml strings.
    """
    marc_xml = _read_content_or_path(marc_xml)

    return type_decisioner(
        marc_xml,
        lambda: transform_to_mods_mono(marc_xml, uuid, url),
        lambda: transform_to_mods_multimono(marc_xml, uuid, url),
        lambda: transform_to_mods_periodical(marc_xml, uuid, url),
    )
