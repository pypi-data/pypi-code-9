#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from os.path import join
from os.path import dirname

import pytest

from amqp.marcxml2mods import ConversionRequest
from amqp.marcxml2mods import reactToAMQPMessage


# Fixtures ====================================================================
@pytest.fixture
def marc_oai():
    with open(join(dirname(__file__), "oai_example.oai")) as f:
        return f.read()


@pytest.fixture
def converted():
    with open(join(dirname(__file__), "transformed_mods.xml")) as f:
        return f.read()


# Tests =======================================================================
def test_chain(marc_oai, converted):
    res = reactToAMQPMessage(
        ConversionRequest(
            marc_xml=marc_oai,
            uuid="asd",
            url="http://kitakitsune.org"
        ),
        lambda x: x
    )

    # with open("asd.xml", "wt") as f:
    #     f.write(res.mods_files[0])

    assert res.mods_files[0] == converted
