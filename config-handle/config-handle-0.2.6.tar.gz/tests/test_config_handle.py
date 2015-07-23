#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config-handle
----------------------------------

Tests for `config-handle` module.
"""
import pytest
import config_handler
import os

newf = os.tmpfile()

settings = """
[DIR]
dest_dir = /mnt/Archive/backup
src_dir =
"""

newf.write(settings)
newf.seek(0)

conf = config_handler.Parser(file_object='fp',filename=newf)


assert 'DIR' in conf.sections()
assert conf.has_section('DIR')
assert 'dest_dir' in conf.options('DIR')
assert len(conf.options('DIR')) > 0

assert conf.get_setting('DIR','dest_dir') == '/mnt/Archive/backup'
