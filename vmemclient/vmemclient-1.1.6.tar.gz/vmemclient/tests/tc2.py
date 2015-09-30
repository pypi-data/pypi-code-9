import os
import sys
import unittest

import mock

import vmemclient
from vmemclient.core.error import *
import vmemclient.concerto.concerto

import vmemclient.tests.test_concerto01

class TestConcerto02(vmemclient.tests.test_concerto01.TestConcerto01):
    CLASS_UNDER_TEST = vmemclient.concerto.concerto.Concerto02
