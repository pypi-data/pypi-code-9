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

from unittest import TestCase

from watcher_metering_drivers.instance_cpu import InstanceCpuNodePuller


class TestInstanceCpuDrivers(TestCase):

    def test_instance_cpu(self):
        data_puller = InstanceCpuNodePuller(
            InstanceCpuNodePuller.get_name(),
            InstanceCpuNodePuller.get_default_probe_id(),
            InstanceCpuNodePuller.get_default_interval(),
        )
        str(data_puller)
        # for _ in range(10):
        #     time.sleep(1)
        #     print([metric.value for metric in data_puller.do_pull()])
