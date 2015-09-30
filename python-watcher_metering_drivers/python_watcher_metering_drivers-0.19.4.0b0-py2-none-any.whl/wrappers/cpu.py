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

from watcher_metering_drivers.wrappers.virt.instance.base import \
    LibvirtInspector


class InstanceCpuWrapper(LibvirtInspector):

    _timer = getattr(time, 'monotonic', time.time)

    Instance = namedtuple(typename="Instance", field_names=["name", "id"])
    CpuTimeRecord = namedtuple(
        typename="CpuTimeRecord",
        field_names=["cpu_time", "sys_time", "cpu_count"],
    )

    def __init__(self, libvirt_type, libvirt_uri):
        super(InstanceCpuWrapper, self).__init__(libvirt_type, libvirt_uri)
        self._last_sys_cpu_time = None
        self._last_proc_cpu_time = None

        # Contains all last values (CPU times) for each encountered instance
        self._instance_record_cache = {}

    def get_cpu_count(self, instance):
        return self.inspect_cpus(instance).number

    def get_cpu_time(self, instance):
        return self.inspect_cpus(instance).time

    def get_instances(self):
        domains = self._get_connection().listAllDomains()
        return [self.Instance(name=dom.name(), id=dom.UUIDString())
                for dom in domains]

    def _sys_timer(self, num_cpus):
        # POSIX Only !!!!
        return self._timer() * num_cpus

    def record_sample(self, instance, cpu_time_record):
        self._instance_record_cache[instance] = cpu_time_record

    def get_last_record(self, instance):
        return self._instance_record_cache.get(instance)

    def instance_cpu_percent(self, instance, interval=None):
        """Return a float representing the instance process CPU
        utilization as a percentage.
        """
        num_cpus = self.get_cpu_count(instance)
        new_sys_time = self._sys_timer(num_cpus)
        new_cpu_time = self.get_cpu_time(instance)

        last_record = self.get_last_record(instance)
        new_record = self.CpuTimeRecord(
            cpu_time=new_cpu_time,
            sys_time=new_sys_time,
            cpu_count=num_cpus,
        )
        # Save value for next call
        self.record_sample(instance, new_record)

        if not last_record:
            # This means there is ont previous record to work with
            # Hence we cannot sample it yet, so we return a symbolic 0.0%
            return 0.0

        delta_proc = new_record.cpu_time - last_record.cpu_time
        delta_time = new_record.sys_time - last_record.sys_time

        try:
            # The utilization split between all CPUs.
            # Note: a percentage > 100 is legitimate as it can result
            # from a process with multiple threads running on different
            # CPU cores, see:
            # http://stackoverflow.com/questions/1032357
            # https://github.com/giampaolo/psutil/issues/474
            overall_percent = 100 * delta_proc / (delta_time * num_cpus * 10e9)
        except ZeroDivisionError:
            # interval was too low
            return 0.0
        else:
            return round(overall_percent, 1)
