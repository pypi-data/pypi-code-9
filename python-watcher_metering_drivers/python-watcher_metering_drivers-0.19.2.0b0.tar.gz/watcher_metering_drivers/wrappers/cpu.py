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

import time

from collections import namedtuple

import libvirt
from watcher_metering_drivers.wrappers.virt.instance.base import \
    LibvirtInspector


class InstanceCpuWrapper(LibvirtInspector):

    _timer = getattr(time, 'monotonic', time.time)

    Instance = namedtuple(typename="Instance", field_names=["name", "id"])

    def __init__(self, libvirt_type, libvirt_uri):
        super(InstanceCpuWrapper, self).__init__(libvirt_type, libvirt_uri)
        self._last_sys_cpu_time = None
        self._last_proc_cpu_time = None

    def get_cpu_count(self, instance):
        return self.inspect_cpus(instance).number

    def get_cpu_time(self, instance):
        return self.inspect_cpus(instance).time

    def get_conn(self):
        return libvirt.openReadOnly(None)

    def get_instances(self):
        domains = self.get_conn().listAllDomains()
        return [self.Instance(name=dom.name(), id=dom.UUIDString())
                for dom in domains]

    def instance_cpu_percent(self, instance, interval=0.1):
        """Return a float representing the instance process CPU
        utilization as a percentage.
        """
        blocking = interval is not None and interval > 0.0
        num_cpus = self.get_cpu_count(instance)

        def timer():
            # POSIX Only !!!!
            return self._timer() * num_cpus

        if blocking:
            st1 = timer()
            pt1 = self.get_cpu_time(instance)
            time.sleep(interval)
            st2 = timer()
            pt2 = self.get_cpu_time(instance)
        else:
            st1 = self._last_sys_cpu_time
            pt1 = self._last_proc_cpu_time
            st2 = timer()
            pt2 = self.get_cpu_time(instance)
            if st1 is None or pt1 is None:
                self._last_sys_cpu_time = st2
                self._last_proc_cpu_time = pt2
                return 0.0

        delta_proc = (pt2 - pt1)
        delta_time = st2 - st1
        # reset values for next call in case of interval == None
        self._last_sys_cpu_time = st2
        self._last_proc_cpu_time = pt2
        try:
            # The utilization split between all CPUs.
            # Note: a percentage > 100 is legitimate as it can result
            # from a process with multiple threads running on different
            # CPU cores, see:
            # http://stackoverflow.com/questions/1032357
            # https://github.com/giampaolo/psutil/issues/474
            overall_percent = 100 * delta_proc / (delta_time * num_cpus * 10e9)
            # overall_percent = ((delta_proc / delta_time) * 100) * num_cpus
        except ZeroDivisionError:
            # interval was too low
            return 0.0
        else:
            return round(overall_percent, 1)
