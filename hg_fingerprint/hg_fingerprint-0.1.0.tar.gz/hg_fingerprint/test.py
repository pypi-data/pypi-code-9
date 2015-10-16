# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.bitbucket@metagriffin.net>
# date: 2015/10/15
# copy: (C) Copyright 2015-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest
import collections

#------------------------------------------------------------------------------
class TestHgFingerprint(unittest.TestCase):

  sample_metadata = collections.OrderedDict([
    ('repo',                'dca7d15bf04445e0a3136d5ce5cfa034e5cfa034'),
    ('node',                '6d881282ad46412ead8ad83e074ce451074ce451'),
    ('branch',              'default'),
    ('latesttags',          ['blue', 'moon']),
    ('latesttagdistance',   7),
    ('timestamp',           '2009-02-13T23:31:30Z'),
  ])

  #----------------------------------------------------------------------------
  def test_text(self):
    from . import md2text
    self.assertEqual(
      md2text(None, self.sample_metadata),
      'repo: dca7d15bf04445e0a3136d5ce5cfa034e5cfa034\n'
      'node: 6d881282ad46412ead8ad83e074ce451074ce451\n'
      'branch: default\n'
      'latesttag: blue\n'
      'latesttag: moon\n'
      'latesttagdistance: 7\n'
      'timestamp: 2009-02-13T23:31:30Z\n'
    )

  #----------------------------------------------------------------------------
  def test_json(self):
    from . import md2json
    self.assertEqual(
      md2json(None, self.sample_metadata),
      '{"repo": "dca7d15bf04445e0a3136d5ce5cfa034e5cfa034",'
      ' "node": "6d881282ad46412ead8ad83e074ce451074ce451",'
      ' "branch": "default",'
      ' "latesttags": ["blue", "moon"],'
      ' "latesttagdistance": 7,'
      ' "timestamp": "2009-02-13T23:31:30Z"}\n'
    )

  #----------------------------------------------------------------------------
  def test_yaml(self):
    from . import md2yaml
    # note: converting to dict because yaml serializes that...
    #       so, need to ensure handling arbitrary order...
    self.assertEqual(
      sorted(md2yaml(None, dict(self.sample_metadata)).split('\n')),
      sorted((
        'repo: dca7d15bf04445e0a3136d5ce5cfa034e5cfa034\n'
        'node: 6d881282ad46412ead8ad83e074ce451074ce451\n'
        'branch: default\n'
        'latesttags: [blue, moon]\n'
        'latesttagdistance: 7\n'
        'timestamp: \'2009-02-13T23:31:30Z\'\n'
      ).split('\n'))
    )

  #----------------------------------------------------------------------------
  def test_xml(self):
    from . import md2xml
    # note: converting to dict because yaml serializes that...
    #       so, need to ensure handling arbitrary order...
    self.assertEqual(
      md2xml(None, self.sample_metadata),
      '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
      '<fingerprint>'
      '<repo>dca7d15bf04445e0a3136d5ce5cfa034e5cfa034</repo>'
      '<node>6d881282ad46412ead8ad83e074ce451074ce451</node>'
      '<branch>default</branch>'
      '<latesttag>blue</latesttag>'
      '<latesttag>moon</latesttag>'
      '<latesttagdistance>7</latesttagdistance>'
      '<timestamp>2009-02-13T23:31:30Z</timestamp>'
      '</fingerprint>'
    )

  #----------------------------------------------------------------------------
  def test_hg_fingerprint(self):
    # TODO: implement...
    raise unittest.SkipTest('testing :hg:`fingerprint` not implemented')

  #----------------------------------------------------------------------------
  def test_hg_archive(self):
    # TODO: implement...
    raise unittest.SkipTest('testing monkeypatching of :hg:`archive` not implemented')


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
