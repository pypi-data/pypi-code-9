#! /usr/bin/envb python

# http://stackoverflow.com/questions/12003805/threadsafe-and-fault-tolerant-file-writes

import logtool, os, tempfile

class AtomicTempFile (object): # pylint: disable=R0903

  @logtool.log_call
  def __init__(self, final_path, **kwargs):
    tmpfile_dir = kwargs.pop ('dir', None)
    if tmpfile_dir is None:
      tmpfile_dir = os.path.dirname (final_path)
    self.tmpfile = tempfile.NamedTemporaryFile (dir = tmpfile_dir, **kwargs)
    self.final_path = final_path
    # FIXME: Initialise the tempfile with the prior content?

  @logtool.log_call
  def __getattr__ (self, attr):
    return getattr (self.tmpfile, attr)

  @logtool.log_call
  def __enter__ (self):
    self.tmpfile.__enter__ ()
    return self

  @logtool.log_call
  def __exit__ (self, exc_type, exc_val, exc_tb):
    if exc_type is None:
      self.tmpfile.delete = False
      self.tmpfile.__exit__ (exc_type, exc_val, exc_tb)
      os.rename (self.tmpfile.name, self.final_path)
