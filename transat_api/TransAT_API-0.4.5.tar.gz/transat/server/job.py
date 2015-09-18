from transat.config import ascomp_setup as setup

global_config = setup.install()


class Job(object):
    def __init__(self, wd, nprocs, fun):
        self.wd = wd
        self.nprocs = nprocs
        self.fun = fun

    def run(self):
        try:
          worker = "local"
          transat = global_config.get_software('transat')
          if self.fun == "run_init":
              _ = transat.run('compile_init', worker, {'wd': self.wd})
              status = transat.run('run_init', worker, {'wd': self.wd, 'nprocs': self.nprocs})
          else:
              status = transat.run('run', worker, {'wd': self.wd, 'nprocs': self.nprocs})

        except:
            pass
