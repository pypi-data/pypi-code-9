# -*- encoding: utf-8 -*-
# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from oslo_config import cfg


AGENT_OPTS = (
    cfg.BoolOpt(
        'use_nanoconfig_service',
        default=True,
        required=True,
        help='Whether it should connect to the publisher via nanoconfig '
             'or directly.',
    ),
    cfg.StrOpt(
        'nanoconfig_profile',
        default="nanoconfig://watcher-metering-agent",
        required=True,
        help='Profile name to be requested to the nanoconfig service. '
             'Should always take the form: nanoconfig://{PROFILE_NAME}',
    ),
    cfg.StrOpt(
        'nanoconfig_service_endpoint',
        default="",  # Extracts it from the environment variable by default
        required=True,
        help='Nanoconfig service endpoint. By default, extracted from the '
             '"NN_CONFIG_SERVICE" environment variable',
    ),
    cfg.StrOpt(
        'nanoconfig_update_endpoint',  # see NN_CONFIG_UPDATES
        default="",  # Extracts it from the environment variable by default
        required=True,
        help='Nanoconfig update service endpoint. By default, extracted from '
             'the "NN_CONFIG_UPDATES" environment variable',
    ),
    cfg.StrOpt(
        'publisher_endpoint',
        default="tcp://127.0.0.1:12345",
        required=True,
        help='Publisher endpoint. Used if the `use_nanoconfig_service` option '
             'is not activated',
    ),
    cfg.ListOpt(
        'driver_names',
        default=[],
        required=True,
        sample_default='cpu_count,disk_free',
        help='List of driver names the agent will dynamically spin up.'
    ),
)

AGENT_GROUP_NAME = "agent"


def register_agent_opts(conf):
    conf.register_opts(AGENT_OPTS, group=AGENT_GROUP_NAME)


def list_opts():
    return [
        (AGENT_GROUP_NAME, AGENT_OPTS),
    ]
