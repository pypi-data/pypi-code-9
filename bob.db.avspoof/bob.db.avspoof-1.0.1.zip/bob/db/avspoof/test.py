#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
#
# Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks on the protocols of a subset of the AVspoof database
"""

import bob.db.avspoof

def test_query():
  db = bob.db.avspoof.Database()

  assert len(db.client_ids()) == 194 # 194 client ids for world, dev and eval
  assert len(db.client_ids(groups='world')) == 150 # 150 client ids for world
  assert len(db.client_ids(groups='optional_world_1')) == 150 # 150 client ids for optional world 1
  assert len(db.client_ids(groups='optional_world_2')) == 150 # 150 client ids for optional world 2
  assert len(db.client_ids(groups='dev')) == 44 # 44 client ids for dev
  assert len(db.client_ids(groups='eval')) == 44 # 44 client ids for eval

  assert len(db.model_ids()) == 194 # 30 model ids for world, dev and eval
  assert len(db.model_ids(groups='world')) == 150 # 10 model ids for world
  assert len(db.model_ids(groups='optional_world_1')) == 150 # 150 model ids for optional world 1
  assert len(db.model_ids(groups='optional_world_2')) == 150 # 150 model ids for optional world 2
  assert len(db.model_ids(groups='dev')) == 44 # 44 model ids for dev
  assert len(db.model_ids(groups='eval')) == 44 # 44 model ids for eval

  assert len(db.objects(groups='world')) == 20600 # 20600 samples in the world set

  assert len(db.objects(groups='dev', purposes='enroll')) == 2198 # 2198 samples for enrollment in the dev set
  assert len(db.objects(groups='dev', purposes='enroll', model_ids='m001')) == 53 # 53 samples to enroll model 'm001' in the dev set
  assert len(db.objects(groups='dev', purposes='probe')) == 2099 # 300 samples as probes in the dev set

  assert len(db.objects(groups='eval', purposes='enroll')) == 2198 # 1509 samples for enrollment in the eval set
  assert len(db.objects(groups='eval', purposes='enroll', model_ids='m001')) == 53 # 53 samples to enroll model 'm001' in the eval set
  assert len(db.objects(groups='eval', purposes='probe')) == 176320 # 176320 samples as probes in the eval set

