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

import os
import unittest
import collections
from contextlib import contextmanager
import tempfile
import tarfile
import shutil
import subprocess
import json
import xml.etree.ElementTree as ET

import six
from six.moves import shlex_quote
from aadict import aadict

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
    from .. import md2_text
    self.assertEqual(
      md2_text(None, self.sample_metadata),
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
    from .. import md2_json
    self.assertEqual(
      md2_json(None, self.sample_metadata),
      '{"repo": "dca7d15bf04445e0a3136d5ce5cfa034e5cfa034",'
      ' "node": "6d881282ad46412ead8ad83e074ce451074ce451",'
      ' "branch": "default",'
      ' "latesttags": ["blue", "moon"],'
      ' "latesttagdistance": 7,'
      ' "timestamp": "2009-02-13T23:31:30Z"}\n'
    )

  #----------------------------------------------------------------------------
  def test_yaml(self):
    from .. import md2_yaml
    # note: converting to dict because yaml serializes that...
    #       so, need to ensure handling arbitrary order...
    self.assertEqual(
      sorted(md2_yaml(None, dict(self.sample_metadata)).split('\n')),
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
    from .. import md2_xml
    # note: converting to dict because yaml serializes that...
    #       so, need to ensure handling arbitrary order...
    self.assertEqual(
      md2_xml(None, self.sample_metadata),
      '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
      '<fingerprint>'
      '<repo>dca7d15bf04445e0a3136d5ce5cfa034e5cfa034</repo>'
      '<node>6d881282ad46412ead8ad83e074ce451074ce451</node>'
      '<branch>default</branch>'
      '<latesttag>blue</latesttag>'
      '<latesttag>moon</latesttag>'
      '<latesttagdistance>7</latesttagdistance>'
      '<timestamp>2009-02-13T23:31:30Z</timestamp>'
      '</fingerprint>\n'
    )

  repo_01_metadata = dict(
    repo              = 'd4af185dabbfc61c06726c8a3f90574e9b242a70',
    node              = '963c62e3873155a0d30de61d2b089b560304cada',
    branch            = 'default',
    latesttags        = ['null'],
    latesttagdistance = 2,
  )

  repo_01_metadata_flat = (
    ('repo',             'd4af185dabbfc61c06726c8a3f90574e9b242a70'),
    ('node',             '963c62e3873155a0d30de61d2b089b560304cada'),
    ('branch',           'default'),
    ('latesttag',        'null'),
    ('latesttagdistance', 2),
  )

  #----------------------------------------------------------------------------
  @contextmanager
  def repo_rc_env(self, repo, hgrc):
    # TODO: this currently requires that hg_fingerprint be installed
    #       exploded... fix!
    hgfpdir = os.path.dirname(os.path.dirname(__file__))
    tdir = tempfile.mkdtemp(prefix='test.hg_fingerprint.', suffix='.repo')
    tarfile.open(os.path.join(hgfpdir, 'test', repo + '.tgz')).extractall(tdir)
    fp = tempfile.NamedTemporaryFile(
      mode='wb', prefix='test.hg_fingerprint.', suffix='.hgrc', delete=False)
    hgrc_ext = '''\
[extensions]
fingerprint = {hg_fingerprint_dir}
'''.format(hg_fingerprint_dir=hgfpdir)
    fp.write(hgrc_ext)
    fp.write(hgrc)
    fp.close()
    yield aadict(
      env     = dict(HGRCPATH=shlex_quote(fp.name)),
      repodir = tdir,
    )
    os.unlink(fp.name)
    shutil.rmtree(tdir)

  #----------------------------------------------------------------------------
  def runhg(self, args, context, input=None):
    proc = subprocess.Popen(
      ['hg', '--cwd', context.repodir] + args,
      stdin  = subprocess.PIPE,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      env    = context.env,
    )
    (out, err) = proc.communicate(input=input)
    if err:
      raise ValueError('hg returned with error: ' + err)
    return out

  #----------------------------------------------------------------------------
  def test_hg_fingerprint(self):
    with self.repo_rc_env('repo-01', '') as context:
      output = self.runhg(['fingerprint', '--format', 'json', '--no-date'], context)
    self.assertEqual(
      json.loads(output),
      self.repo_01_metadata)

  #----------------------------------------------------------------------------
  def test_hg_archive_default(self):
    with self.repo_rc_env('repo-01', '''
[fingerprint]
timestamp = false
''') as context:
      tardat = self.runhg(['archive', '--type', 'tar', '--prefix', '.', '-'], context)
    tfile = tarfile.open(fileobj=six.BytesIO(tardat))
    self.assertEqual(
      sorted(tfile.getnames()),
      ['./.hg_archival.txt', './readme.txt', './zogzog'])
    fdat = tfile.extractfile(tfile.getmember('./.hg_archival.txt')).read()
    self.assertEqual(
      sorted([line for line in fdat.split('\n') if line]),
      sorted([k + ': ' + str(v) for k, v in self.repo_01_metadata_flat]))

  #----------------------------------------------------------------------------
  def test_hg_archive_json(self):
    with self.repo_rc_env('repo-01', '''
[fingerprint]
path = fingerprint.json
timestamp = false
''') as context:
      tardat = self.runhg(['archive', '--type', 'tar', '--prefix', '.', '-'], context)
    tfile = tarfile.open(fileobj=six.BytesIO(tardat))
    self.assertEqual(
      sorted(tfile.getnames()),
      ['./fingerprint.json', './readme.txt', './zogzog'])
    fdat = tfile.extractfile(tfile.getmember('./fingerprint.json')).read()
    self.assertEqual(
      json.loads(fdat),
      self.repo_01_metadata)

  #----------------------------------------------------------------------------
  def test_hg_archive_multifp(self):
    with self.repo_rc_env('repo-01', '''
[fingerprint]
path = fingerprint.json .meta/info.xml
timestamp = false
''') as context:
      tardat = self.runhg(['archive', '--type', 'tar', '--prefix', '.', '-'], context)
    tfile = tarfile.open(fileobj=six.BytesIO(tardat))
    self.assertEqual(
      sorted(tfile.getnames()),
      ['./.meta/info.xml', './fingerprint.json', './readme.txt', './zogzog'])
    fdat = tfile.extractfile(tfile.getmember('./fingerprint.json')).read()
    self.assertEqual(
      json.loads(fdat),
      self.repo_01_metadata)
    xdat = ET.fromstring(tfile.extractfile(tfile.getmember('./.meta/info.xml')).read())
    self.assertEqual(
      sorted((x.tag, x.text) for x in xdat),
      sorted((k, str(v)) for k,v in self.repo_01_metadata_flat))


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
