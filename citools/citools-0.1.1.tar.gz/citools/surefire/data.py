# coding=utf-8

"""

   Copyright 2015 Andreas Würl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

class TestSuite(object):
    def __init__(self, name, tests, skipped, failures, errors, time, testcases, properties):
        self.name = name
        self.tests = int(tests)
        self.skipped = int(skipped)
        self.failures = int(failures)
        self.errors = int(errors)
        self.time = float(time)
        self.testcases = testcases
        self.properties = properties


class TestCase(object):
    def __init__(self, classname, name, time, failure=None):
        self.name = name
        self.classname = classname
        self.time = float(time)
        self.failure = failure


class Failure(object):
    def __init__(self, message, type):
        self.message = message
        self.type = type
