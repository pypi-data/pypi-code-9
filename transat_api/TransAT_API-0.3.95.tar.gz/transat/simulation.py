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

logger = logging.getLogger(__name__)

from transat.database import database as db
from transat.worker.worker import Worker
from transat.software.software import Software
from transat.software.installation import Installation
from transat.setup.setup import Setup
from transat.server.client import Client

from transat.config import ascomp_setup as setup

global_config = setup.install()


class Error(Exception):
    """Base class for exceptions in this module

    Args:
        msg (str): Human readable string describing the exception.
        code (int, optional): Error code, defaults to 2.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, msg, code=2):
        self.msg = msg
        self.code = code


class Simulation(object):
    """TransAT simulation project

    A simulation object contains all the data related to a TransAT project
    (setup, inputs, workflow, individual tasks, result data, etc...)

    """

    def __init__(self, name="simulation"):
        """Construct new Simulation

        Args:
            database (Database): database into which simulation results are stored

        Returns:
            Simulation: new simulation object

        """
        self.postprocess_script = dict()
        self.name = name.replace(' ', '_')
        self.db = db.Database(name, global_config.env['path']['db'])
        self.defaultworker = Worker('localhost')
        self.postprocess = None  # will be populated by a Software() object
        self.setup = None  # will be populated by a Setup() object
        self.current = 'local'
        self.base_folder = global_config.env['wd']['local']
        self.change_dict = {}

        logger.info('Simulation object created')

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
        return self.db.store_path(key, data)

    def load_path(self, key):
        return os.path.abspath(self.db.load_path(key))

    def load(self, key):
        """Load object from database

        All types of objects can be stored and retrieved

        Args:
            key (str): Primary key

        Returns:
            Data: data stored under this key for the current simulation object

        Raises:
            Error: on database read error

        """
        # TODO: make the key unique. E.g. something like key = self.id + '@' + key
        return self.db.load(key)

    def load_template(self, dirname):
        """Load a setup from a template, typically created using a GUI

        The setup can contain keyword parameters for some input values

        Args:
            dirname (str): path to the project directory

        Returns:
            bool: True if successful

        """

        if not os.path.exists(dirname):
            import transat

            path = os.path.dirname(transat.__file__)
            dirname = os.path.join(path, dirname)

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

    def set_folder(self, folder, worker_names):
        for worker in worker_names:
            base = global_config.env['wd'][worker]
            f = os.path.join(base, self.name, folder)
            self.store_path(worker, f)

    def set_number_of_timestep(self, ntime):
        self.change_inputs({'ntimet': str(ntime)}, file_name='transat_mb.inp')

    def set_fluid_properties(self, densities, viscosities):
        for name in densities.keys():
            self.change_inputs({'rho_' + name: densities[name]}, file_name='transat_mb.inp')
        for name in viscosities.keys():
            self.change_inputs({'nu_' + name: viscosities[name]}, file_name='transat_mb.inp')

    def load_fluid_properties(self, filename, phase):
        """Load a file describing the fluid properties for a given phase

        The file can be in JSON or XML format

        Args:
            filename (str): path to the file containing the fluid data.
            phase (str): Name of the phase

        Returns:
            bool: True if successful

        TODO:
            Description of file format accepted by TransAT

        """
        # self.materials.load(filename, phase)
        pass

    def prepare_simulation_files(self):
        """Write the input files for TransAT solvers

        This function should be run after the template is loaded and after all the parameters have been changed

        Returns:
            bool: True if successful

        """
        logger.info('Preparing simulation files')

        self.setup.write()  # bcs._write_bcs_in_stt()
        self._apply_changes_to_inputs()
        stt_files = glob.glob(os.path.join(self.load_path('local'), '*.stt'))
        project_name = os.path.basename(stt_files[0])
        tui = global_config.get_software('transatui')
        tui.run('prepare_simulation_files', 'local',
                {'project_name': project_name, 'wd': self.load_path('local')})

        logger.info('Done preparing simulation files')

    def add_geometry(self, cylinders):
        """Add CAD objects to the simulation

        Args:
            cylinders (list of cylinders): objects to be added

        Returns:
            bool: True if successful

        """
        # TODO: Extend this function for generic CAD objects

        bboxes = []
        margin = 0
        centerlines = []
        for cylinder, i in zip(cylinders, range(len(cylinders))):
            bboxes.append(self.create_pipe(cylinder, name="cylinder" + str(i + 1) + ".stl"))
            margin = cylinder['r'] if margin < cylinder['r']  else margin
            normal = cylinder['normal'] / np.linalg.norm(cylinder['normal'])
            centerlines.append(cylinder['base'])
            centerlines.append(np.array(cylinder['base']) + np.multiply(cylinder['H'], normal))
        self.pipe_network = centerlines
        dimensions = self.get_dimensions(bboxes, margin=margin)
        stt_case = glob.glob(os.path.join(self.load_path(self.current), '*.stt'))[0]
        stt_case = os.path.basename(stt_case)
        self.change_inputs(dimensions, file_name=stt_case)

    def create_pipe(self, cylinder, name):
        cad = global_config.get_software('cad')
        return cad.run('create_cylinder', 'local',
                       {'path': self.load_path('local'), 'name': name, 'cylinder': cylinder})

    @staticmethod
    def _add_margin(box, names, margin=5):
        for j in range(len(names)):
            name = names[j]
            if 'min' in name:
                box[j] -= margin
            else:
                box[j] += margin
        return box

    def get_dimensions(self, boxes, margin=5):
        # TODO
        # fix overlapping strategy
        dimensions = {}
        names = ['xmin', 'ymin', 'zmin', 'xmax', 'ymax', 'zmax']
        for i in range(len(boxes)):
            box = self._add_margin(boxes[i], names, margin)
            for j in range(len(names)):
                name = names[j]
                dim = box[j]
                dimensions[name + str(i + 1)] = dim

        dimensions['xmin3'] += 2 * margin
        dimensions['xmax2'] -= 2 * margin
        dimensions['xmin2'] = dimensions['xmax1']
        dimensions['xmax3'] = dimensions['xmin1']

        for direction in ['x', 'y', 'z']:
            values = []
            for key in dimensions.keys():
                if key.startswith(direction):
                    values.append(dimensions[key])
            dimensions[direction + 'min'] = min(values)
            dimensions[direction + 'max'] = max(values)

        return dimensions

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

    def change_inputs(self, changes, file_name):
        """Change parameters of the current project

        This is typically used to modify a setup that was loaded from a template

        Args:
            changes (dict): inputs to be changed

        Returns:
            bool: True if successful

        Note:
            The changes are not actually applied until :func:`prepare_simulation_files` is called.

        Examples:
            Changing the total number of iterations to 123:

            >>> changes = {'ntime': '123'}
            >>> sim.change_inputs(changes, file_name='transat_mb.inp')

        See Also:
            :func:`load_template`

        """
        if file_name in self.change_dict.keys():
            self.change_dict[file_name].update(changes)
        else:
            self.change_dict[file_name] = changes

    def _apply_changes_to_inputs(self):
        for file_name, changes in self.change_dict.iteritems():
            filename = os.path.join(self.load_path('local'), file_name)
            with open(filename, 'r') as f:
                data = f.read()

            data = data.format(**changes)
            with open(filename, 'w') as f:
                f.writelines(data)

    def run_init(self, worker=None, nprocs=1, url=None):
        """Initialize TransAT simulation

        Compile and run the initial conditions

        Args:
            worker (Worker, optional): Worker where the task will be executed, default to localhost

        Returns:
            bool: True if successful

        """
        if worker is None:
            worker = self.defaultworker

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

    def run(self, worker=None, nprocs=1, url=None):
        """Run TransAT simulation to steady state

        Solve steady flow equations using TransAT.

        Args:
            worker (Worker, optional): Worker where the task will be executed, default to localhost

        Returns:
            bool: True if successful

        """
        if worker is None:
            worker = self.defaultworker

        self._pull_data(location=worker)
        wd = self.load_path(self.current)

        print "Running steady state simulation on " + worker
        if url is None:
            transat = global_config.get_software('transat')
            status = transat.run('run', worker, {'wd': wd, 'name': self.name, 'nprocs': nprocs})
        else:
            client = Client(address=url)
            client.run(wd=os.path.abspath(wd), nprocs=nprocs)

        self._push_data(location=worker)

    def run_until(self, time, worker, nprocs):
        """Run TransAT unsteady simulation from the current state until a given time

        Solve unsteady flow equations using TransAT.

        Args:
            time (double): Time until which the simulation should run (physical time, in seconds)
            worker (Worker, optional): Worker where the task will be executed, default to localhost
            nprocs (int, optional): Number of processors to be used, default to one

        Returns:
            bool: True if successful

        """
        # TODO
        self._pull_data(location=worker)
        self._push_data(location=worker)
        pass

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

        Returns:
            bool: True if successful

        """
        worker = global_config.get_worker(worker_name)
        myfuns = self._get_module(module_name)
        self.postprocess = Software(name='postprocess', actions=[f[0] for f in myfuns])
        pol = Installation(self.postprocess, worker)
        self.postprocess.add_installation(pol)
        for myfun in myfuns:
            pol.define_action_as_fun(myfun[0], fun=myfun[1])

    def _transfer_data(self, src, dest):
        """Transfer data between two workers

        Extended description of function.

        Args:
            src  (Worker): Worker where the data is
            dest (Worker): Worker where the data should go

        Returns:
            bool: True if the transfer was successful

        """

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
