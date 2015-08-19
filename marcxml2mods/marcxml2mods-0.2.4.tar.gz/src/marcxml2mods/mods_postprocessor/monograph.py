#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from functools import wraps

import dhtmlparser
from dhtmlparser import first
from remove_hairs import remove_hairs

from shared_funcs import insert_tag
from shared_funcs import transform_content
from shared_funcs import double_linked_dom


# Functions & objects =========================================================
def add_xml_declaration(fn):
    """
    Decorator to add header with XML version declaration to output from FN.
    """
    @wraps(fn)
    def add_xml_declaration_decorator(*args, **kwargs):
        return '<?xml version="1.0" encoding="UTF-8"?>\n\n' + fn(
            *args,
            **kwargs
        )

    return add_xml_declaration_decorator


def get_mods_tag(dom):
    """
    Find and return HTMLElement with ``<mods:mods>`` tag from the `dom`.
    """
    return first(dom.find("mods:mods"))


def add_missing_xml_attributes(dom, volume_counter=0):
    """
    Add `xmlns` and `ID` attributes to ``<mods:mods>`` tag.

    Args:
        dom (HTMLElement): DOM containing whole document.
        volume_counter (int, default 0): ID of volume.
    """
    mods_tag = get_mods_tag(dom)

    if mods_tag:
        params = mods_tag.params

        # add missing attributes
        params["ID"] = "MODS_VOLUME_%04d" % (volume_counter + 1)
        params["xmlns:mods"] = "http://www.loc.gov/mods/v3"
        params["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        params["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        params["xsi:schemaLocation"] = " ".join((
            "http://www.w3.org/2001/XMLSchema-instance",
            "http://www.w3.org/2001/XMLSchema.xsd",
            "http://www.loc.gov/mods/v3",
            "http://www.loc.gov/standards/mods/v3/mods-3-4.xsd",
            "http://www.w3.org/1999/xlink http://www.w3.org/1999/xlink.xsd",
        ))


def fix_invalid_type_parameter(dom):
    """
    "Make sure that ``<mods:placeTerm>`` has ``type="code"`` attribute.
    """
    # fix invalid type= paramater
    placeterm_tag = dom.match(
        "mods:originInfo",
        "mods:place",
        ["mods:placeTerm", {"authority": "marccountry"}]
    )
    if placeterm_tag:
        first(placeterm_tag).params["type"] = "code"


def add_uuid(dom, uuid):
    """
    Add ``<mods:identifier>`` with `uuid`.
    """
    mods_tag = get_mods_tag(dom)

    uuid_tag = dhtmlparser.HTMLElement(
        "mods:identifier",
        {"type": "uuid"},
        [dhtmlparser.HTMLElement(uuid)]
    )

    insert_tag(uuid_tag, dom.find("mods:identifier"), mods_tag)


def add_marccountry_tag(dom):
    """
    Add ``<mods:placeTerm>`` tag with proper content.
    """
    marccountry = dom.find("mods:placeTerm", {"authority": "marccountry"})

    # don't add again if already defined
    if marccountry:
        return

    marccountry_tag = dhtmlparser.HTMLElement(
        "mods:place",
        [
            dhtmlparser.HTMLElement(
                "mods:placeTerm",
                {"type": "code", "authority": "marccountry"},
                [dhtmlparser.HTMLElement("xr-")]
            )
        ]
    )
    insert_tag(
        marccountry_tag,
        dom.match("mods:mods", "mods:originInfo", "mods:place"),
        first(dom.find("mods:originInfo"))
    )


def add_genre(dom):
    """
    Add ``<mods:genre>`` with `electronic volume` content into
    ``<mods:originInfo``.
    """
    mods_tag = get_mods_tag(dom)

    matched_genres = [
        "electronic title",
        "electronic volume",
    ]
    genre = dom.find(
        "mods:genre",
        fn=lambda x: x.getContent().lower().strip() in matched_genres
    )

    if not genre:
        genre_tag = dhtmlparser.HTMLElement(
            "mods:genre",
            [dhtmlparser.HTMLElement("electronic volume")]
        )
        insert_tag(genre_tag, dom.find("mods:originInfo"), mods_tag)


def remove_hairs_from_tags(dom):
    """
    Use :func:`.remove_hairs` to some of the tags:

        - mods:title
        - mods:placeTerm
    """
    transform_content(
        dom.match("mods:mods", "mods:titleInfo", "mods:title"),
        lambda x: remove_hairs(x.getContent())
    )
    transform_content(
        dom.match(
            "mods:originInfo",
            "mods:place",
            ["mods:placeTerm", {"type": "text"}]
        ),
        lambda x: remove_hairs(x.getContent())
    )


def fix_issuance(dom):
    """
    Fix <mods:issuance> for monographic tags from `monographic` to
    `single_unit`.
    """
    transform_content(
        dom.match(
            "mods:originInfo",
            {
                "tag_name": "mods:issuance",
                "fn": lambda x: x.getContent() == "monographic"
            }
        ),
        lambda x: "single unit"
    )


def fix_location_tag(dom):
    """
    Repair the <mods:location> tag (the XSLT template returns things related to
    paper books, not electronic documents).
    """
    location = dom.match(
        "mods:mods",
        "mods:location",
    )

    # if no location tag found, there is nothing to be fixed
    if not location:
        return
    location = first(location)

    # fix only <mods:location> containing <mods:physicalLocation> tags
    if not location.find("mods:physicalLocation"):
        return

    url = location.find("mods:url", {"usage": "primary display"})

    # parse URL
    if url:
        url = first(url).getContent()
    else:
        urls = filter(
            lambda x: x.getContent(),
            location.find("mods:url")
        )

        if not urls:
            return

        url_tag = max(urls, key=lambda x: len(x.getContent()))
        url = url_tag.getContent()

    # replace the code with new tag
    replacer = dhtmlparser.parseString("""
  <mods:location>
    <mods:holdingSimple>
      <mods:copyInformation>
        <mods:electronicLocator>""" + url + """</mods:electronicLocator>
      </mods:copyInformation>
    </mods:holdingSimple>
  </mods:location>
    """)

    location.replaceWith(
        first(replacer.find("mods:location"))
    )

    dhtmlparser.makeDoubleLinked(dom)


def fix_related_item_tag(dom):
    """
    Remove <mods:relatedItem> tag in case that there is only <mods:location>
    subtag.
    """
    location = dom.match(
        "mods:mods",
        "mods:relatedItem",
        "mods:location"
    )

    if not location:
        return
    location = first(location)

    location.replaceWith(
        dhtmlparser.HTMLElement()
    )

    # remove whole <mods:relatedItem> tag, if there is nothing else left in it
    related_item = dom.match(
        "mods:mods",
        "mods:relatedItem"
    )
    related_item = first(related_item)

    if not related_item.getContent().strip():
        related_item.replaceWith(dhtmlparser.HTMLElement())


def fix_missing_electronic_locator_tag(dom, url):
    """
    In case that MODS contains no URL and the location is wrong (physical), add
    url from `url` parameter.
    """
    electronic_locator = dom.match(
        "mods:mods",
        "mods:location",
        "mods:holdingSimple",
        "mods:copyInformation",
        "mods:electronicLocator",
    )
    # do not try to fix correct records
    if electronic_locator:
        return

    # if no location tag found, add it
    location = dom.match("mods:mods", "mods:location")
    if location:
        location = first(location)
    else:
        location_tag = dhtmlparser.parseString(
            "<mods:location></mods:location>"
        )

        insert_tag(
            location_tag,
            dom.find("mods:recordInfo"),
            dom.find("mods:mods")
        )

        location = first(dom.match("mods:mods", "mods:location"))

    replacer = dhtmlparser.parseString("""
  <mods:location>
    <mods:holdingSimple>
      <mods:copyInformation>
        <mods:electronicLocator>""" + url + """</mods:electronicLocator>
      </mods:copyInformation>
    </mods:holdingSimple>
  </mods:location>
    """)

    location.replaceWith(
        first(replacer.find("mods:location"))
    )


@add_xml_declaration
def postprocess_monograph(mods, uuid, counter, url):
    """
    Fix bugs in `mods` produced by XSLT template.

    Args:
        mods (str): XML string generated by XSLT template.
        uuid (str): UUID of the package.
        counter (int): Number of record, is added to XML headers.
        url (str): URL of the publication (public or not).

    Returns:
        str: Updated XML.
    """
    dom = double_linked_dom(mods)

    add_missing_xml_attributes(dom, counter)
    fix_invalid_type_parameter(dom)

    if uuid:
        add_uuid(dom, uuid)

    add_marccountry_tag(dom)

    # add <genre> tag if not found
    add_genre(dom)

    # remove hairs from some tags
    remove_hairs_from_tags(dom)

    fix_issuance(dom)
    fix_location_tag(dom)
    fix_related_item_tag(dom)

    fix_missing_electronic_locator_tag(dom, url)

    return dom.prettify()
