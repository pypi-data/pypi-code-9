# coding: utf-8
import logging
import os
import time
import json
import cStringIO
import traceback
import copy

__author__ = 'czhou <czhou@ilegendsoft.com>'

Log = logging.getLogger("Leap")
Log.addHandler(logging.StreamHandler())
Log.setLevel(logging.DEBUG)