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


class NamedElement(object):

    def __init__(self):
        self.uuid = ""
        self.human_id = ""

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_human_id(self, id):
        self.human_id = id

    def get_human_id(self):
        return self.human_id

    def __str__(self):
        return "[" + str(self.uuid) + "]"
