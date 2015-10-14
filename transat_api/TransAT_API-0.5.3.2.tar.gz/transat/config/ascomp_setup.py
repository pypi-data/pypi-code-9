import os
import sys
from transat.worker.cluster import Cluster
from transat.worker.worker import Worker
from transat.software.software import Software
from transat.software.installation import Installation
from transat.config.globalconfig import GlobalConfig
from transat.communicator.communicator import Communicator
from transat.setup.cad import CAD
from transat.config import user_setup as usetup
import glob
import ctypes

def load_paraview(path_package, path_bin):
    p = os.path.normpath(path_package)
    sys.path.append(p)

    p = os.path.normpath(os.path.join(path_package, 'vtk'))
    sys.path.append(p)
    p = os.path.normpath(os.path.join(path_package, 'paraview'))
    sys.path.append(p)

    p = os.path.normpath(path_bin)
    if os.name == "nt":
        if 'path' in os.environ.keys():
            os.environ['path'] += p+";"
        elif 'PATH' in os.environ.keys():
            os.environ['PATH'] += p+";"
        else:
            os.environ['PATH'] = p+";"
    key_name = "LD_LIBRARY_PATH"
    if (key_name not in os.environ.keys()) or (path_bin not in os.environ[key_name]):
            print "Please add "+str(path_bin)+" to LD_LIBRARY_PATH"

def get_python_cmd(path, cmd):
    cmd = os.path.join(path, cmd)
    cmd = [sys.executable, os.path.normpath(cmd)]
    return cmd


def define_cluster(env, transat, util):
    host = env['remote']['host']
    user = env['remote']['username']

    # define utility used to communicate data and execute remote commands
    com = Communicator(host=host, username=user)
    calanda = Cluster(host=host, username=user)

    # configure software programs on each worker
    utility = Installation(util, calanda, env=env)
    utility.define_action_as_fun('upload', fun=com.upload)
    utility.define_action_as_fun('download', fun=com.download)
    utility.define_action_as_fun('rsync', fun=com.rsync)
    utility.define_action_as_fun('exec', fun=com.run_cmd)

    toc = Installation(transat, calanda)
    toc.define_action_as_fun('remove_init', fun=com.run_cmd,
                             arg={'cmd': 'rm transatmbinitialDP'})
    toc.define_action('compile_init',
                      cmd='source /etc/profile ;' + os.path.join(env['tmb_path']['calanda'], 'tmb_init_compile.py'),
                      wrapper=calanda.ssh)
    toc.define_action('run_init', cmd='mpirun -n {nprocs} ./transatmbinitialDP',
                      wrapper=calanda.qsub)
    toc.define_action('run', cmd='mpirun -n {nprocs} {transat_path}/transatmbDP',
                      arg={'transat_path': env['tmb_path']['calanda']},
                      wrapper=calanda.qsub)

    return toc, utility


def install():
    # define local environment variables
    env = usetup.load()

    # initialize freecad
    freecad = CAD(freecad_path=env['path']['freecad'])

    # define available computing resources (aka workers)
    local = Worker('local')

    # define available software codes
    transat = Software(name='transat', actions=['remove_init',
                                                'compile_init',
                                                'run_init',
                                                'run'])
    transatui = Software(name='transatui', actions=['prepare_simulations_files'])
    util = Software(name='utility', actions=['upload', 'download', 'exec'])
    cad = Software(name='cad', actions=['create_cylinder'])

    cadl = Installation(cad, local)
    cadl.define_action_as_fun('create_cylinder', fun=freecad.create_cylinder)

    tui = Installation(transatui, local)
    cmd = get_python_cmd(env['path']['ui'], 'transatui.py')
    cmd += ['--Graphics', 'bash', '--Project']
    tui.define_action_as_fun('prepare_simulation_files', fun=local.prepare_simulation_files,
                             arg={'cmd': cmd})

    tol = Installation(transat, local)
    tol.define_action_as_fun('remove_init', fun=local.remove_file,
                             arg={'filename': 'transatmbinitialDP'})

    cmd = get_python_cmd(env['tmb_path']['local'], 'tmb_init_compile.py')
    tol.define_action('compile_init', cmd=cmd)
    cmd = get_python_cmd(env['tmb_path']['local'], 'tmb_runinit.py')
    cmd += ['-n', '{nprocs}']
    tol.define_action('run_init', cmd=cmd)
    cmd = get_python_cmd(env['tmb_path']['local'], 'tmb_run.py')
    cmd += ['-n', '{nprocs}']
    tol.define_action('run', cmd=cmd)

    installations = [tol, tui, cadl]

    if "remote" in env.keys():
        toc, utility = define_cluster(env, transat, util)
        installations += [toc, utility]

    if "paraview" in env.keys():
        load_paraview(env['paraview']['site-packages'], env['paraview']['shared'])

    return GlobalConfig(installations, [transat, transatui, util, cad], env)

