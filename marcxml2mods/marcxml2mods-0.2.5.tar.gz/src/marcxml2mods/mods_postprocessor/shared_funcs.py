#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser
from dhtmlparser import first


# Functions & classes =========================================================
def insert_tag(tag, before, root):
    """
    Insert `tag` before `before` tag if present. If not, insert it into `root`.

    Args:
        tag (obj): HTMLElement instance.
        before (obj): HTMLElement instance.
        root (obj): HTMLElement instance.
    """
    if not before:
        root.childs.append(tag)
        tag.parent = root
        return

    if type(before) in [tuple, list]:
        before = first(before)

    # check that `before` is double linked
    if not hasattr(before, "parent"):
        raise ValueError("Input must be double-linked!")

    # put it before first existing identifier
    parent = before.parent
    parent.childs.insert(
        parent.childs.index(before),
        tag
    )
    tag.parent = parent


def transform_content(tags, content_transformer):
    """
    Transform content in all `tags` using result of `content_transformer(tag)`
    call.

    Args:
        tags (obj/list): HTMLElement instance, or list of HTMLElement
                         instances.
        content_transformer (function): Function which is called as
                                        ``content_transformer(tag)``.
    """
    if type(tags) not in [tuple, list]:
        tags = [tags]

    for tag in tags:
        new_child = dhtmlparser.HTMLElement(content_transformer(tag))

        # don't forget to add parent if the list is double-linked
        if hasattr(tag, "parent"):
            new_child.parent = tag

        tag.childs = [new_child]


def double_linked_dom(str_or_dom):
    """
    Create double linked DOM from input.

    In case of string, parse it, make it double-linked. In case of DOM, just
    make it double-linked.

    Args:
        str_or_dom (str/HTMLelement): String or HTMLelement instance.

    Returns:
        obj: HTMLelement with parsed, double-linked content from `str_or_dom`.
    """
    dom = str_or_dom
    if not isinstance(str_or_dom, dhtmlparser.HTMLElement):
        dom = dhtmlparser.parseString(str_or_dom)

    dhtmlparser.makeDoubleLinked(dom)

    return dom
