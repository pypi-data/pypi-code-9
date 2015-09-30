# -*- encoding: utf-8 -*-
# Copyright (c) 2015 b<>com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import platform
from unittest import TestCase

from ddt import data
from ddt import ddt
from ddt import unpack
from freezegun import freeze_time
from mock import Mock
from mock import patch
import psutil
from psutil._common import sswap
from watcher_metering.agent.measurement import Measurement
from watcher_metering_drivers import swap


@ddt
class TestSwapDrivers(TestCase):

    fake_swap = sswap(
        total=17099124736,
        used=10,
        free=17099124726,
        percent=0.0,
        sin=0,
        sout=0)

    SCENARIOS = (
        (swap.TotalSwapPuller,
         patch.object(psutil, "swap_memory", Mock(return_value=fake_swap)),
         Measurement(
             name="compute.node.swap.total",
             timestamp="2015-08-04T15:15:45.703542+00:00",
             unit="bytes",
             type_="gauge",
             value=17099124736,
             resource_id="test_node",
             host="test_node",
             resource_metadata={
                 "host": "test_node",
                 "title": "swap_total"
             }
         )),
        (swap.FreeSwapPuller,
         patch.object(psutil, "swap_memory", Mock(return_value=fake_swap)),
         Measurement(
             name="compute.node.swap.free",
             timestamp="2015-08-04T15:15:45.703542+00:00",
             unit="bytes",
             type_="gauge",
             value=17099124726,
             resource_id="test_node",
             host="test_node",
             resource_metadata={
                 "host": "test_node",
                 "title": "swap_free"
             }
         )),
        (swap.UsedSwapPuller,
         patch.object(psutil, "swap_memory", Mock(return_value=fake_swap)),
         Measurement(
             name="compute.node.swap.used",
             timestamp="2015-08-04T15:15:45.703542+00:00",
             unit="bytes",
             type_="gauge",
             value=10,
             resource_id="test_node",
             host="test_node",
             resource_metadata={
                 "host": "test_node",
                 "title": "swap_used"
             }
         )),
    )

    @unpack
    @data(*SCENARIOS)
    @freeze_time("2015-08-04T15:15:45.703542+00:00")
    @patch.object(platform, "node", Mock(return_value="test_node"))
    def test_swap(self, puller_factory, swap_patch, expected_data):
        data_puller = puller_factory(
            puller_factory.get_name(),
            puller_factory.get_default_probe_id(),
            puller_factory.get_default_interval(),
        )

        with swap_patch:
            pulled_data = data_puller.do_pull()

        self.assertEqual(
            [measurement.as_dict() for measurement in pulled_data],
            [expected_data.as_dict()]
        )
