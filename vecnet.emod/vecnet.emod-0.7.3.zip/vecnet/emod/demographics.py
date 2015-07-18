#!/usr/bin/python
#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import collections
import os


def generate_attribute_substitution():
    for first_char in "abcdefghijklmnopqrstuvwxyz":
        for second_char in "abcdefghijklmnopqrstuvwxyz":
            yield "%s%s" % (first_char, second_char)
    yield None


def compile_node(node, string_table, string_table_generator):
    """ Compile node and all it's subnodes
    :param node:
    :param string_table:
    :param string_table_generator:
    :return:
    """
    compiled_node = {}
    if not isinstance(node, dict):
        return node

    for attribute in node:
        attribute_substitution = string_table.get(attribute, None)
        if attribute_substitution is None:
            attribute_substitution = string_table_generator.next()
            string_table[attribute] = attribute_substitution
        if attribute_substitution is None:
            raise RuntimeError("There is currently an implicit limit of 676 different demographic attribute-name "
                               "strings that can be used.  ")
        if isinstance(node[attribute], dict):
            compiled_node[attribute_substitution] = compile_node(node[attribute], string_table, string_table_generator)
        elif isinstance(node[attribute], list):
            compiled_node[attribute_substitution] = \
                [compile_node(item, string_table, string_table_generator) for item in node[attribute]]
        else:
            compiled_node[attribute_substitution] = node[attribute]
    return compiled_node


def compile_demographics(demographics_filename, compiled_demographics_filename=None, is_contents=False):
    """ Produce compiled demographics file (demographics.compiled.json)
    Can't use name "compile" because there is a build-in function with this name
    https://docs.python.org/2/library/functions.html#compile

    :param demographics_filename:
    :param compiled_demographics_filename:
    :return:
    """
    if is_contents:
        demographics_json = json.loads(demographics_filename)
    else:
        # Compiled JSON Demographics file format is defined in EMOD Documentation
        # http://idmod.org/idmdoc/#DTKv1_6/v1_6FileFormatLayouts/Compiled JSON File Format.htm
        if compiled_demographics_filename is None:
            compiled_demographics_filename = demographics_filename + ".compiled.json"
    
        with open(demographics_filename) as fp:
            demographics_json = json.load(fp)

    # compile Nodes section
    # StringTable will be populated as we go
    compiled_nodes = []
    string_table = collections.OrderedDict()
    # Initialize generator for attribute substitutions ("aa", "ab", etc)
    string_table_generator = generate_attribute_substitution()

    for node in demographics_json["Nodes"]:
        compiled_node = compile_node(node, string_table, string_table_generator)
        compiled_nodes.append(compiled_node)

    # Compile Defaults section if available
    if "Defaults" in demographics_json:
        compiled_defaults = compile_node(demographics_json["Defaults"], string_table, string_table_generator)
    else:
        compiled_defaults = None

    # Populate sections in compiled demographics file in certain order
    compiled_demographics_json = collections.OrderedDict()
    compiled_demographics_json["Metadata"] = demographics_json["Metadata"]
    compiled_demographics_json["StringTable"] = string_table
    if compiled_defaults is not None:
        compiled_demographics_json["Defaults"] = compiled_defaults
    nodes_section_offset = len(json.dumps(compiled_demographics_json)) - 2  # remove trailing "]}"
    compiled_demographics_json["Nodes"] = compiled_nodes

    # Generate NodeOffsets
    # Note we cannot change file after NodeOffsets are calculated
    node_offsets = ""
    current_offset = 0
    for node in compiled_nodes:
        node_len = len(json.dumps(node))
        node_offsets += "%0.8X%0.8X" % (node[string_table["NodeID"]], current_offset + nodes_section_offset)
        current_offset += node_len + 1  # Including comma (,)
    compiled_demographics_json["NodeOffsets"] = node_offsets
    return json.dumps(compiled_demographics_json)


def decompile_node(node, string_table):
    """
    Decompile an array or a dictionary using mapping define by demographics["StringTable"]
    :param node:
    :param string_table:
    :return: same type as node
    """

    # TableString dictionary looks like
    # "IndividualAttributes":"aa", ..
    # We want a reverse translation "aa" -> "IndividualAttributes"
    reversed_string_table = dict(map(reversed, string_table.items()))

    if isinstance(node, dict):
        # Decompile each item in this dictionary
        decompiled_node = dict()
        for i in node:
            decompiled_node[reversed_string_table[i]] = decompile_node(node[i], string_table)
        return decompiled_node
    elif isinstance(node, list):
        # If this is an array, we should try decompiling every dictionary inside (nested decompilation, LOL)
        # Using list comprehension just to show off
        return [decompile_node(item, string_table) for item in node]
    else:
        # It is a number or a string - just return it
        return node


def decompile_demographics(compiled_demographics_filename, is_contents=False):
    """
    Note this function assumes that compiled demographics file is a valid JSON document. It is true for files
    generated by compiledemog.py script. Based on my understanding of compiled demographics file may not be always true,
    but I have never seen compiled demographics that was not a valid JSON.

    Compiled JSON Demographics file format is defined in EMOD Documentation
    http://idmod.org/idmdoc/Content/EMOD/FileFormatLayouts/Compiled%20JSON%20File%20Format.htm

    originally this function was named "decompile", but renamed to "decompile_demographics" for consistency with
    function name "compile_demographics"

    :param compiled_demographics_filename:
    :return: content of decompiled demographics file as a string
    :rtype: str
    """
    
    if is_contents:
        compiled_demographics_json = json.loads(compiled_demographics_filename)
    else:
        with open(compiled_demographics_filename) as fp:
            compiled_demographics_json = json.load(fp)

    demographics_json = {
        "Metadata": compiled_demographics_json["Metadata"],
        "Nodes": [decompile_node(node, compiled_demographics_json["StringTable"])
                  for node in compiled_demographics_json["Nodes"]]
    }
    if "Defaults" in compiled_demographics_json:
        demographics_json["Defaults"] = decompile_node(compiled_demographics_json["Defaults"],
                                                       compiled_demographics_json["StringTable"])
    return json.dumps(demographics_json)


if __name__ == "__main__":
    print decompile_demographics(os.path.join("tests",
                                              "demographics",
                                              "tb_vital_dynamics_test_complex_demographics.compiled.json"))
    print decompile_demographics(os.path.join("tests",
                                              "demographics",
                                              "demographics.compiled.json"))
    print decompile_demographics(os.path.join("tests",
                                              "demographics",
                                              "solomons",
                                              "Honiara_Haleta_two_node_demographics.compiled.json"))
