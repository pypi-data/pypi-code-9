"""
Top-level module for TransAT simulation projects
"""

import os
import sys
import shutil
import distutils.dir_util
import errno
import uuid
import inspect
import numpy as np
import glob
import logging
import threading
import time
from progressbar import Bar, ETA, Percentage, ProgressBar, ReverseBar, RotatingMarker

logger = logging.getLogger(__name__)

from transat.database import database as db
from transat.worker.worker import Worker
from transat.software.software import Software
from transat.software.installation import Installation
from transat.setup.setup import Setup
from transat.server.client import Client
from transat.postproc.postprocessing import Postprocessing
from transat.server.server import Server

from transat.config import ascomp_setup as setup

global_config = setup.install()


class Error(Exception):
    def __init__(self, msg, code=2):
        self.msg = msg
        self.code = code


class Simulation(object):
    """TransAT simulation project

    A simulation object contains all the data related to a TransAT project
    (setup, inputs, workflow, individual tasks, result data, etc...)

    """

    def __init__(self, name="simulation", folder=None):
        """Construct new Simulation with default worker (local).

        Args:
            name (String): name of the simulation.

        Returns:
            Simulation: new simulation object

        """
        self.postprocess_script = dict()
        self.name = name.replace(' ', '_')
        self.db = db.Database(name, global_config.env['path']['db'])
        self.defaultworker = Worker('local')
        self.postprocess = Postprocessing(self)  # will be populated by a Software() object
        self.setup = None  # will be populated by a Setup() object
        self.current = 'local'
        self.url = None
        self.base_folder = global_config.env['wd']['local']
        self.change_dict = {}
        logger.info('Simulation object created')
        if folder is not None:
            self.set_folder(folder)

    def store(self, key, data):
        """Store data into database

        The data are stored into the database associated with this simulation.
        It is stored using a primary key.

        Args:
            key (str): Primary key (private to the current simulation object)
            data (Data): Data to be stored

        Returns:
            bool: Description of return value

        Raises:
            Error: on database write error

        """
        # TODO: make the key unique. E.g. something like key = self.id + '@' + key
        self.db.store(key, data)

    def store_path(self, key, data):
        """Store path into database

        The paths of the simulation is stored in the database for all the workers.

        Args:
            key (str): worker name
            data (str): path

        Returns:
            bool: Success

        """

        return self.db.store_path(key, data)

    def load_path(self, worker_name="local"):
        """Load path from the database

        Retrive the path for a worker in the database

        Args:
            worker_name (str): worker name

        Returns:
            str: path

        """
        return os.path.abspath(self.db.load_path(worker_name))


    def load(self, key):
        """Load object from database

        All types of objects can be stored and retrieved

        Args:
            key (str): Primary key

        Returns:
            Data: data stored under this key for the current simulation object

        """
        # TODO: make the key unique. E.g. something like key = self.id + '@' + key
        return self.db.load(key)

    def load_case(self, dirname):
        """Load a case, typically created using a GUI

        It is necessary to start a simulation object with a template and then to modify it using the API.
        If the directory given as input does not exist in the current directory (where the python command is launched),
        the function will go in the installation folder and look in the provided templates.

        Args:
            dirname (str): path to the project directory

        """

        return self.load_template(dirname)

    def load_template(self, dirname):
        """Load a setup from a template, typically created using a GUI

        It is necessary to start a simulation object with a template and then to modify it using the API.
        If the directory given as input does not exist in the current directory (where the python command is launched),
        the function will go in the installation folder and look in the provided templates.

        Args:
            dirname (str): path to the project directory

        """
        if not os.path.exists(dirname):
            import transat
            old_dirname = dirname
            path = os.path.dirname(transat.__file__)
            dirname = os.path.join(path, dirname)

        if not os.path.isdir(dirname):
            print "Could not find a template folder in folders"
            print "\t"+old_dirname
            print "\t"+dirname
            print "Aborting execution"
            sys.exit()

        try:
            f = self.load_path('local')
        except KeyError:
            folder = uuid.uuid4()
            f = os.path.join(self.base_folder, str(folder))
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)
        try:
            distutils.dir_util.copy_tree(dirname, f)
            # shutil.copytree(dirname, f)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(dirname, f)
            else:
                raise

        logger.info('Simulations is stored on local at ' + f)
        self.setup = Setup(f)
        self._push_data('local')
        self.store_path('local', f)

    def set_folder(self, folder, worker_names=["local"], base_folder=None):
        """Allow the user to set a folder name where the simulation files will be stored

        By default unique Ids are generated for the folders name. If set_folder is called, the simulation will be saved
        in thw working_directory defined in user_config.ini.
        typically it will have the following path: /{wd}/{Simulation_Name}/{folder}

        Args:
            folder (str): folder name
            worker_name (str): name of the worker on which this folder should be used

        """
        if len(self.db.get_workers_with_path()) != 0:
            print "set_folder() should be called before load_template()"
            print "aborting"
            sys.exit()

        for worker in worker_names:
            base = None
            if worker == "local":
                base = base_folder
            if base is None:
                base = global_config.env['wd'][worker]
            f = os.path.join(base, self.name, folder)
            self.store_path(worker, f)

    def set_number_of_timestep(self, ntime):
        """Define the number of time step of the simulation

        Set the number of time step for which the unsteady simulation will run.

        Args:
            ntime (int): number of time-steps

        """

        self.setup.input.set_nbr_timestep(ntime)
        self.setup.write()


    def set_nbr_iteration(self, maxit=100000):
        """


        Args:

        """

        self.setup.input.set_maxit(maxit)
        self.setup.input.set_maxit_max(maxit)
        self.setup.write()




    def set_final_time(self, time, ntime=100000):
        """Define the final physical time of the simulation

        Set the target final physical time for which the unsteady simulation will run.
        A value for the the number of time steps is also set (by default to 100000)

        Args:
            time (float): physical time
            ntime (int):  maximum number of time-steps

        """
        self.setup.input.set_final_time(time)
        self.setup.input.set_nbr_timestep(ntime)
        self.setup.write()
        self.setup.input.write()

    def set_fluid_properties(self, densities, viscosities):
        """Define the fluid properties of the phases

        Given two dictionaries of viscosities and densities with their phase name as keys.

        Args:
            densities (dict): density [kg/m^3]
            viscosities (dict):  dynamic viscosity [Pa.s]

        """
        phases = self.setup.input.get_phases()
        for name in densities.keys():
            phase = phases.get_phase(name)
            phase.set_density(densities[name])
            phase.set_viscosity(viscosities[name])

    def load_fluid_properties(self, filename, phase):
        # self.materials.load(filename, phase)
        pass

    def prepare_simulation_files(self):
        """Write the input files for TransAT solvers

        This function should be run after the template is loaded and after all the parameters have been changed

        """
        logger.info('Preparing simulation files')
        self.setup.input.enable_3d_output()

        self.setup.write()  # bcs._write_bcs_in_stt()
        stt_files = glob.glob(os.path.join(self.load_path('local'), '*.stt'))
        project_name = os.path.basename(stt_files[0])
        tui = global_config.get_software('transatui')
        tui.run('prepare_simulation_files', 'local',
                {'project_name': project_name, 'wd': self.load_path('local')})

        logger.info('Done preparing simulation files')

    def get_bc(self, name):
        """Get a Boundary Condition object by name

        The name of the boundary condition refers to the label of that boundary condition
        in TransAT GUI

        Args:
            name (str): name (or label) of the boundary condition, as in TransAT GUI

        Returns:
            transat.setup.bc.BC: Boundary Condition object

        See Also:
            The list of available boundary conditions is returned by the function :func:`get_bc_names`

        """
        return self.setup.bcs.get_bc(name)

    def get_bc_names(self):
        """Get the list of all Boundary Conditions by name

        The names of the boundary condition refer to the label of these boundary conditions
        in TransAT GUI

        Args:
            name (str): name (or label) of the boundary condition, as in TransAT GUI

        Returns:
            transat.setup.bc.BC: Boundary Condition object

        See Also:
            To access a given Boundary Condition object, use the  :func:`get_bc` function

        """
        return self.setup.bcs.get_bc_names()

    def get_phase(self, name="Phase 1"):
        """Get phase by name

        Args:
            name (str): name (or label) of the phase, as in TransAT GUI

        Returns:
            transat.setup.input.Phase: Phase object

        """
        return self.setup.input.get_phase(name)

    def set_dx(self, dx):
        """Set cell size

        The value dx is applied in x,  y and z direction.

        Args:
            dx (float): grid size in meter

        """
        return self.setup.mesher.set_dx(dx)

    def make_2D(self, axis="z", bc_name="symmetry"):
        """Set cell size

        Makes the domain 2D and reduces the axis direction to 2*offset (2*1e-7) and
        set boundary conditions to the surfaces normal to axis usually a symmetry type BC

        Args:
            axis (string): axis in which the direction is reduced
            bc_name (string): name of the bc that should by applied to surface normal to axis
        """
        axes = ['x', 'y', 'z']
        axes.remove(axis)
        tree = self.setup.bcs.get_surface_tree()
        tree.get_surface_with_normal(axis).set_bc_name(bc_name)
        self.setup.mesher.set_2D(axes[0], axes[1])


    def run_init(self, worker=None, nprocs=1, url=None):
        """Initialize TransAT simulation

        Compile and run the initial conditions. If URL is passed it will run it on TransAT-Server.

        Args:
            worker (Worker, optional): Worker where the task will be executed, default to localhost
            nprocs (int, optional): Number of processor
            url (str, optional): URL of the TransAT-server

        """
        if worker is None:
            worker = self.defaultworker.name

        self._pull_data(location=worker)
        wd = self.load_path(self.current)
        print "Running initial conditions on " + worker

        if url is None:
            transat = global_config.get_software('transat')
            #_ = transat.run('remove_init', worker, {'wd': wd})
            _ = transat.run('compile_init', worker, {'wd': wd})
            status = transat.run('run_init', worker, {'wd': wd, 'name': self.name, 'nprocs': nprocs})
        else:
            client = Client(address=url)
            client.run_init(wd=os.path.abspath(wd), nprocs=nprocs)

        self._push_data(location=worker)

    def run(self, worker=None, nprocs=1, url=None, nbrIterations=1000):
        """Run TransAT simulation to steady state

        Run TransAT solver. If URL is passed it will run it on TransAT-Server.

        Args:
            worker (Worker, optional): Worker where the task will be executed, default to localhost
            nprocs (int, optional): Number of processor
            url (str, optional): URL of the TransAT-server
            nbrIterations (int, optional): number of iterations

        """

        self.set_nbr_iteration(nbrIterations)
        if worker is None:
            worker = self.defaultworker.name

        self._pull_data(location=worker)
        wd = self.load_path(self.current)

        print "Running steady state simulation on " + worker
        if url is None:
            if self.url is None:
                self._lauch_server()
            url = self.url

        client = Client(address=url)
        client.run(wd=os.path.abspath(wd), nprocs=nprocs)
        # wait until simulation is finished
        self._watch(url)

        self._push_data(location=worker)

    def run_until(self, time, worker=None, nprocs=1, url=None):

        """Run TransAT unsteady simulation from the current state until a given time

        Solve unsteady flow equations using TransAT.
        If URL is passed it will run it on TransAT-Server.

        Args:
            time (float): Physical time (sec) at which the simulation should stop
            worker (Worker, optional): Worker where the task will be executed, default to localhost
            nprocs (int, optional): Number of processor
            url (str, optional): URL of the TransAT-server

        """

        self.set_final_time(time, 10000)

        if worker is None:
            worker = self.defaultworker.name

        self._pull_data(location=worker)
        wd = self.load_path(self.current)

        print "Running simulation on " + worker
        if url is None:
            if self.url is None:
                self._lauch_server()
            url = self.url

            #transat = global_config.get_software('transat')
            #status = transat.run('run', worker, {'wd': wd, 'name': self.name, 'nprocs': nprocs})
        #else:
        client = Client(address=url)
        client.run(wd=os.path.abspath(wd), nprocs=nprocs)
        # wait until simulation is finished
        self._watch(url)
        self._push_data(location=worker)

    def run_postprocess(self, *args, **kwargs):
        # TODO: improve documentation
        """ run a postprocessing function

        The postprocessing functions are entirely user-defined and can take any number of arguments

        Args:
            *args (list of arguments): List of arguments, the first of which *must* be the name of the function to call
            **kwargs (dict): keyword arguments

        Returns:
            bool: True if successful

        Examples:
            The following example runs the function *plot_pressure* on the local workstation,
            using arguments that are passed to the function:

            >>>  sim.run_postprocess('plot_pressure',
            ...                      worker_name='local',
            ...                      args={'points': sim.pipe_network,
            ...                            'folder': sim.load('local')}
            ...                     )

        See Also:
            The postprocessing functions must have been previously loaded using the
            function :func:`add_postprocess`

        """
        if 'worker_name' in kwargs:
            worker_name = kwargs['worker_name']
        else:
            worker_name = None
        self._pull_data(location=worker_name)

        data = self.postprocess.run(*args, **kwargs)

        self._push_data(location=worker_name)
        return data

    def add_postprocess(self, module_name, worker_name='local'):
        """ register a postprocessing module for use with this simulation object

        Extended description of function.

        Args:
            module_name (str): path to the postprocessing module
            worker_name (str optional): name of the worker, default is local

        """
        worker = global_config.get_worker(worker_name)
        myfuns = self._get_module(module_name)
        self.postprocess = Software(name='postprocess', actions=[f[0] for f in myfuns])
        pol = Installation(self.postprocess, worker)
        self.postprocess.add_installation(pol)
        for myfun in myfuns:
            pol.define_action_as_fun(myfun[0], fun=myfun[1])

    def _lauch_server(self):
        se = Server()
        server = threading.Thread(target=se.run)
        server.daemon = True
        server.start()
        self.url = se.get_address()
        return self.url


    def _watch(self, url):

      widgets = ['Simulation: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
             ' ', ETA(), ' ']
      pbar = ProgressBar(widgets=widgets, maxval=10000).start()

      isSteady = self.setup.input.isSteady()

      start = time.time()
      cl = Client(url)
      remaining = 0.0
      while cl.has_jobs():
          elapsed = (time.time() - start)

          if isSteady:
            current_iteration = cl.get_current_iteration()
            remaining = self.setup.input.get_nbr_iterations()-current_iteration
            if current_iteration != 0:
                remaining = remaining/current_iteration*elapsed
          else:
            remaining = cl.get_remaining_time()*60.0
          percentage = elapsed/(elapsed+remaining)*10000
          pbar.update(percentage)
          time.sleep(1)
      pbar.finish()

    def _transfer_data(self, src, dest):

        util = global_config.get_software('utility')

        try:
            dest_path = self.load_path(dest)
        except KeyError:
            _id = uuid.uuid4()
            dest_path = os.path.join(global_config.env['wd'][dest], str(_id))
            self.store_path(dest, dest_path)
        src_path = self.load_path(src)

        if src == 'local':
            remote = dest
        else:
            remote = src
        print "transfering data"
        print src
        print src_path
        print dest
        print dest_path
        util.run('rsync', remote, args={'src': {'worker': src, 'path': src_path},
                                        'dest': {'worker': dest, 'path': dest_path}})
        self.current = dest

    def _pull_data(self, location):
        # ask where the data are
        current = self.load('data_location')

        # fetch the data if necessary
        if current != location:
            self._transfer_data(src=current, dest=location)

        # register where the data now are
        self.store('data_location', location)

    def _push_data(self, location):
        # register where the data now are
        self.store('data_location', location)

    @staticmethod
    def _get_module(module_name):
        path = os.path.dirname(module_name)
        module_name = os.path.basename(module_name)
        module_name = module_name.split('.')[0]
        sys.path.append(path)
        try:
            mod = __import__(module_name)
            all_functions = inspect.getmembers(mod, inspect.isfunction)
        except:
            print("Failed to import module")
            all_functions = {}
        mod = __import__(module_name)
        all_functions = inspect.getmembers(mod, inspect.isfunction)
        return all_functions
