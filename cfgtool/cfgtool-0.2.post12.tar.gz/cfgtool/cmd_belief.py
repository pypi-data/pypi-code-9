#!/usr/bin/env python

import json, logging, logtool
from cfgtool.cmdbase import CmdBase

LOG = logging.getLogger (__name__)

class Action (CmdBase):

  @logtool.log_call
  def run (self):
    self.report (json.dumps (self.belief, indent = 2))
    return 0
