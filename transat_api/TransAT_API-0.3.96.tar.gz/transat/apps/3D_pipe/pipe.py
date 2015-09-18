from transat.simulation import Simulation
import transat.appbuilder as appbuilder
from transat.server.server import Server
import threading
from transat.server.client import Client
import time
import os
from transat.setup.cad import Pipe
from transat.setup.cad import Network
from transat.config import ascomp_setup as setup
from transat.setup.cad import CAD
global_config = setup.install()

app = appbuilder.App('3D_Pipe')
app.add_input('radius', unit='m')


def create_pipe(pipe_radius = 0.25):
    cad = CAD(freecad_path=global_config.env['path']['freecad'])

    pipe = Pipe(name="pipe.stl", radius=pipe_radius)
    pipe.add_point([0, 0.0, 0])
    pipe.add_point([10, 0.0, 0])

    network = Network(cad, [pipe])
    return network, pipe

def get_postprocess_path(name):
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    return os.path.join(path, name)



def my_fun(args):

    sim = Simulation("3D_Pipe")
    # simulations is saved in {local_wd}/Pipe/test_pipe
    sim.set_folder('test_pipe', ['local'])

    # load templates. It will first look in the relative directory
    # and then in the installation directory
    sim.load_template('templates/network_single')

    radius = float(args['radius'])

    network, pipe = create_pipe(radius)
    network.create(path=sim.load_path('local'))

    print sim.load_path('local')

    sim.setup.mesher.set_blocks(network.get_blocks())
    sim.setup.mesher.split_blocks()
    sim.setup.ist.add(network.get_pipes_name())

    sim.setup.mesher.set_dx(radius / 5.0)

    sim.setup.bcs.get_bc('inflow').set_velocities([0.001, 0, 0])

    tree = sim.setup.bcs.create_surfaces_tree()
    tree.get_all_surfaces().set_bc_name('wall')

    tree.get_surface_with_point(pipe.get_inlet_point()).set_bc_name('inflow')
    tree.get_surface_with_point(pipe.get_outlet_point()).set_bc_name('outflow')

    sim.prepare_simulation_files()


    sim.run_init(worker='local', nprocs=2)
    sim.run(worker='local', nprocs=2)


    y = sim.setup.mesher.get_center('y')
    z = sim.setup.mesher.get_center('z')
    x1 = sim.setup.mesher.get_min('x')
    x2 = sim.setup.mesher.get_max('x')
    points = [[x1, y, z], [x2, y, z]]

    sim.add_postprocess(get_postprocess_path("pipe_postprocess.py"))
    sim.run_postprocess('plot_pressure',
                        worker_name='local',
                        args={'points': points,
                              'folder': sim.load_path('local')})

app.add_main(my_fun)

if __name__ == '__main__':
    args = app.parse_inputs()
    app.run(args)
