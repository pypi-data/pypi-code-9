#!/usr/bin/env python

import importlib, json, logging, logtool, re, string, socket
from addict import Dict
from path import Path
from cfgtool.main import CONFIG, CmdError
from cfgtool.cmdio import CmdIO

LOG = logging.getLogger (__name__)
VARIABLE_REGEX = r"\$\{([A-Za-z0-9._:]+)\}"
ESCAPED_REGEX = r"\$\{\{([A-Za-z0-9._:]+)\}\}"
COLOUR_ERROR = "red"
COLOUR_INFO = "white"
COLOUR_INFO_BAD = "magenta"
COLOUR_WARN = "yellow"
COLOUR_REPORT = "green"
COLOUR_FIELDNAME = "cyan"
COLOUR_VALUE = "green"

@logtool.log_call
def is_iterable (i):
  try:
    iter (i)
    return True
  except TypeError:
    return False

@logtool.log_call
def implementation (this, **kwargs):
  cmd = importlib.import_module ("cfgtool.cmd_%s" % this)
  item = getattr (cmd, "Action")
  return item (kwargs).run ()

class CmdBase (CmdIO):

  @logtool.log_call
  def __init__ (self, kwargs, module_not_present = False):
    super (CmdBase, self).__init__ (kwargs)
    self.re_var = re.compile (VARIABLE_REGEX)
    self.re_escvar = re.compile (ESCAPED_REGEX)
    self.kwargs = Dict (kwargs)
    self.conf = CONFIG
    self.belief = Dict ()
    self.cfgfiles = []
    self.info ("Module: %s" % kwargs["module"])
    self.debug ("  work_dir: %s" % self.conf.work_dir)
    self.debug ("  module_dir: %s" % self.conf.module_dir)
    self.debug ("  belief_dir: %s" % self.conf.belief_dir)
    self.load_beliefs ()
    if not module_not_present:
      self.load_cfglist ()

  @logtool.log_call
  def load_beliefs_file (self, target, fname):
    self.debug ("    belief: %s" % fname)
    try:
      target.update (json.loads (file (fname).read ()))
    except Exception as e:
      logtool.log_fault (e)
      self.error ("Error loading belief: %s -- %s" % (fname, e))
      raise ValueError

  @logtool.log_call
  def load_beliefs_dir (self, target, directory):
    files = [f for f in directory.glob (
      "*%s" % self.conf.belief_ext)]
    for fname in sorted (files):
      self.load_beliefs_file (target, fname)

  @logtool.log_call
  def load_beliefs_dirs (self, target, dirs):
    if not isinstance (dirs, str) and is_iterable (dirs):
      for d in dirs:
        self.load_beliefs_dir (target, d)
    else:
      self.load_beliefs_dir (target, dirs)

  @logtool.log_call
  def load_beliefs (self):
    self.load_beliefs_dir (self.belief, self.conf.belief_dir)
    if self.kwargs.module:
      target = self.belief[self.kwargs.module]
      if target.belief_directory:
        self.load_beliefs_dirs (target, target.belief_directory)
      if target.belief_file:
        self.load_beliefs_file (target, target.belief_file)
    else: # load all remotes
      for k, v in self.belief.items ():
        if isinstance (v, dict):
          target = self.belief[k]
          if "belief_directory" in v:
            self.load_beliefs_dirs (target, target.belief_directory)
          if "belief_file" in v:
            self.load_beliefs_file (target, target.belief_file)
    self.belief.update ({
      "LOCAL_HOSTNAME": self.get_localhostname (),
      "LOCAL_STRTIME": self.conf.time_str,
      "LOCAL_UTTIME": self.conf.time_ut,
    })

  @logtool.log_call
  def template_check (self, e):
    if e[0] == "/":
      e = e[1:]
    entry = self.conf.work_dir / e
    fname = Path ("%s%s" % (entry, self.conf.templ_ext))
    if not fname.isfile ():
      self.error ("Template missing: %s" % fname)
      entry = None
    return entry

  @logtool.log_call
  def load_cfglist (self):
    fname = self.conf.module_dir / self.kwargs.module
    if not fname.isfile ():
      self.error ("  %s is not managed by cfgtool" % self.kwargs.module)
      self.info ("    Missing: %s" % fname)
      raise CmdError
    files = [f.strip () for f in fname.lines () if f.strip ()[0] != "#"]
    flist = map (self.template_check, files) # pylint: disable = W0141
    if None in flist:
      raise CmdError
    self.cfgfiles = [f for f in flist if f is not None]

  @logtool.log_call
  def get_localhostname (self):
    return socket.gethostname ().split (".")[0]

  @logtool.log_call
  def get_belief (self, longkey):
    funcmap = {
      ":lower": string.lower,
      ":upper": string.upper,
      ":capitalise": string.capitalize,
      ":capitalize": string.capitalize,
      ":swapcase": string.swapcase,
    }
    key = longkey
    func = None
    for k, v in funcmap.items ():
      if longkey.endswith (k):
        func = v
        key = longkey[:-len (k)]
        break
    keylist = key.split (".")
    rc = reduce (lambda d, k: d[k], keylist, self.belief)
    return rc if func is None else func (rc)

  @logtool.log_call
  def instantiate_file (self, in_file, out_file):
    err = 0
    with file (in_file) as file_in:
      for line in file_in:
        for pattern, re_pat in [("%s%s%s", self.re_var),
                                ("%s${%s}%s", self.re_escvar)]:
          while True:
            m = re_pat.search (line)
            if not m:
              break
            # t = m.group (0) # Entire match
            k = m.group (1) # Variable name
            try:
              v = self.get_belief (k) # Replacement token
              self.debug ("      Mapped: ${%s} -> %s" % (k, v))
            except KeyError:
              v = k
              err += 1
              self.error ("      Undefined: ${%s}" % k)
            line = pattern % (line[:m.start(0)], v, line[m.end(0):])
        out_file.write_text (line, append = True)
    return err

  @logtool.log_call
  def make_file (self, in_file, out_file):
    if not self.conf.nobackup and out_file.isfile ():
      fname = "%s%s.%s" % (out_file, self.conf.backup_ext, self.conf.time_str)
      self.debug ("    Backup: %s -> %s" % (out_file, fname))
      out_file.rename (fname)
    else:
      out_file.remove_p ()
    rc = self.instantiate_file (in_file, out_file)
    if rc:
      self.error ("    Failed.  Some variables were not defined.")
    return rc

  @logtool.log_call
  def compare_files (self, file1, file2):
    if not file1.isfile ():
      self.error ("    Comparison failed: %s is missing" % file1)
      return True
    if not file2.isfile ():
      self.error ("    Comparison failed: %s is missing" % file2)
      return True
    hash1 = file1.read_hexhash ("md5")
    hash2 = file2.read_hexhash ("md5")
    self.debug ("      %s vs %s" % (hash1, hash2))
    rc = hash1 != hash2
    if rc:
      self.error ("    Comparison failed: %s -> %s" % (file1, file2))
    return rc

  @logtool.log_call
  def noop (self, *args):
    pass

  @logtool.log_call
  def process_cfgs (self, lable, cfg_ext, out_ext, func):
    err = 0
    self.report ("  %s" % lable)
    for cfg in self.cfgfiles:
      self.report ("    File: %s" % cfg + out_ext)
      in_file = cfg + cfg_ext
      out_file = cfg + out_ext
      rc = func (in_file, out_file)
      if rc:
        err += 1
        self.error ("      Error in processing: %s" % in_file)
    if err:
      self.error ("  %d files failed to process." % err)
    return err
