"""
This module defines a set of util function used in snakemake workflow.
Currently, this module contains functions for line-based transformations.

Usage
-----

All @linetr decorated function should be called without first parameter (inline).
Decorated function should do the transformation of inline string.
After decoration, a function will be changed to return a new function when called.
This new function will accept a string and will produce a new string.
These functions are transformations used in the `apply` call.

Example:

    from snakemakeutil import del_char_val, del_char_idx, apply

    # Elements of trans list are function which accepts string and return
    # transformed string. These function are created by calling the decorated
    # function with their other parameters (after first mandatory parameter).
    trans = [del_char_val('\x00'), del_char_idx(0)]

    # Transformations are applied to a set of input files and they produce a
    # set of output files. Transformation are applied in the order of
    # definition for each line of each input file.
    apply(trans, "latin1", input, output)
"""

import re


def linetr(orig_f):
    """
    Decorator for line transformation functions. Decorated function should
    accept a string as a first parameter and might have additional arbitrary
    parameters. Function should do some on the input string and produce output
    string or None if the line should be discarded.
    """
    def _innerf(*args, **kwargs):
        def _inner_for_line(inline):
            return orig_f(inline, *args, **kwargs)
        return _inner_for_line
    return _innerf

@linetr
def map_chars(inline, cmap):
    """
    Replaces all characters of the inline string with the values form the
    cmap dict. If the char is not in the map it will remain unchanged.

    Args:
        inline (str): Input string.
        cmap(dict): A dictionary to use for translation.
    """
    return "".join([cmap.get(c, c) for c in inline])

@linetr
def del_char_idx(inline, idx):
    """
    Del char at the position given by the index idx.

    Args:
        inline(str): Input string.
        idx(int): An index position.
    """
    return inline[:idx] + inline[idx+1:]

@linetr
def del_char_val(inline, char):
    """
    Delete all chars matching the given parameter.

    Args:
        inline(str): Input string.
        char(char): A character value which has to be deleted.
    """
    return inline.replace(char, '')

@linetr
def del_line(inline, regex):
    """
    Delete line if it matches given regular expression.

    Args:
        inline(str): Input string.
        regex(str): A regular expression accepted by the re module.
    """
    if re.match(regex, inline):
        return None
    else:
        return inline


def apply(transformations, encoding, in_files, out_files):
    """
    Args:
        transformations(list): A list of callables that accepts a string and
            returns transformed string or None in case line has to be deleted.
        encoding(str): Encoding of files.
        in_files(list): A list of input file names.
        out_files(list): A list of output file names that matches by index with
            the list of input files.
    """
    import codecs
    for idx, infile in enumerate(in_files):
        with codecs.open(infile, encoding=encoding) as in_f:
            with codecs.open(out_files[idx], "w", encoding=encoding) as out_f:
                for line in in_f:
                    for t in transformations:
                        line = t(line)
                        if line is None:
                            break
                    if line is not None:
                        out_f.write(line)



