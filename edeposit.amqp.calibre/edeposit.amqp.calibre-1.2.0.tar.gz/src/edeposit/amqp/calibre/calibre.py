#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
"""
Lowlevel conversion API for calibre's ``ebook-convert``.
"""
import os
import gc
from base64 import b64encode, b64decode
from tempfile import NamedTemporaryFile as NTFile

import sh

from structures import INPUT_FORMATS, OUTPUT_FORMATS, ConversionResponse


# Functions & objects =========================================================
def _wrap(text, columns=80):
    """
    Own "dumb" reimplementation of textwrap.wrap().

    This is because calling .wrap() on bigger strings can take a LOT of
    processor power. And I mean like 8 seconds of 3GHz CPU just to wrap 20kB of
    text without spaces.

    Args:
        text (str): Text to wrap.
        columns (int): Wrap after `columns` characters.

    Returns:
        str: Wrapped text.
    """
    out = []
    for cnt, char in enumerate(text):
        out.append(char)

        if (cnt + 1) % columns == 0:
            out.append("\n")

    return "".join(out)


def convert(input_format, output_format, b64_data):
    """
    Convert `b64_data` fron `input_format` to `output_format`.

    Args:
        input_format (str):  Specification of input format (pdf/epub/whatever),
                             see :attr:`INPUT_FORMATS` for list.
        output_format (str): Specification of output format (pdf/epub/..),
                             see :attr:`OUTPUT_FORMATS` for list.
        b64_data (str):      Base64 encoded data.

    Returns:
        ConversionResponse: `namedtuple` structure with information about \
                            output ``format``, data (``b64_data``) and \
                            ``protocol`` from conversion. Structure is defined\
                            in :class:`.ConversionResponse`.

    Raises:
        AssertionError: When bad arguments are handed over.
        UserWarning: When conversion failed.
    """
    # checks
    assert input_format in INPUT_FORMATS, "Unsupported input format!"
    assert output_format in OUTPUT_FORMATS, "Unsupported output format!"

    with NTFile(mode="wb", suffix="." + input_format, dir="/tmp") as ifile:
        ofilename = ifile.name + "." + output_format

        # save received data to the temporary file
        ifile.write(b64decode(b64_data))
        ifile.flush()

        # free memory from base64 data
        b64_data = None
        gc.collect()

        # convert file
        protocol = ""
        try:
            with NTFile(mode="wb", suffix = ".stdout", dir="/tmp") as stdout:
                sh.ebook_convert(ifile.name, ofilename, _out=stdout).wait()
                stdout.flush()
                protocol = open(stdout.name).read()
                stdout.close()
        except sh.ErrorReturnCode_1, e:
            raise UserWarning(
                "Conversion failed:\n" +
                e.message.encode("utf-8", errors='ignore')
            )

        if output_format.upper() + " output written to" not in protocol:
            raise UserWarning("Conversion failed:\n" + protocol)

        # read the data from the converted file
        output_data = None
        with open(ofilename, "rb") as ofile:
            output_data = _wrap(
                b64encode(ofile.read())
            )
        gc.collect()  # we have experienced unplesant memory spikes

        # remove temporary output file
        os.remove(ofilename)

        return ConversionResponse(
            format=output_format,
            b64_data=output_data,
            protocol=protocol
        )
