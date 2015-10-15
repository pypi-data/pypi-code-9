import transat.appbuilder as appbuilder

from transat.simulation import Simulation

from transat.setup.cad import CAD
from transat.setup.cad import Pipe
from transat.setup.cad import Network

from transat.server.server import Server
import threading
from transat.server.client import Client

import math
import time
import os

from progressbar import Bar, ETA, Percentage, ProgressBar, ReverseBar, RotatingMarker

from transat.config import ascomp_setup as setup

global_config = setup.install()

app = appbuilder.App("Severe Slug")
app.add_input("Radius", unit="m")

def get_postprocess_path(name):
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    return os.path.join(path, name)

def create_pipe(pipe_radius=0.25):
    cad = CAD(freecad_path=global_config.env['path']['freecad'])

    L1 = 20*pipe_radius
    H1 = 4*pipe_radius
    H2 = 4*pipe_radius
    L2 = 10*pipe_radius

    radius = pipe_radius

    pipe = Pipe(name="pipe.stl", radius=pipe_radius, junctions=['open', 'closed'])
    pipe.add_point([0.0, 0.0, 0])
    pipe.add_point([L1, 0.0, 0])

    pipe2 = Pipe(name="pipe2.stl", radius=radius, junctions=['closed', 'open'])
    pipe2.add_point([L1-radius, 0, 0])
    #pipe2.add_point([L1-radius, H1, 0], radius=radius*2) #radius*2)
    #pipe2.add_point([L1+L2-radius, H1, 0])
    pipe2.add_point([L1+L2-radius, 0, 0])

    radius=radius/2

    pipe4 = Pipe(name="pipe4.stl", radius=radius, junctions=['open', 'closed'])
    pipe4.add_point([20*radius, 6*radius, 0])
    pipe4.add_point([20*radius, 0, 0])


    pipe3 = Pipe(name="pipe3.stl", radius=radius, junctions=['closed', 'open'])
    pipe3.add_point([L1-radius, 0, 0])
    pipe3.add_point([L1-radius, -H2, 0], radius=radius*2)
    pipe3.add_point([L1+L2-radius, -H2, 0])

    network = Network(cad, [pipe, pipe2, pipe3, pipe4])

    return network, pipe, pipe2, pipe3, pipe4


def my_fun(inputs):
    radius = float(inputs['Radius'])

    sim = Simulation("Asymmetric")
    # simulations is saved in {local_wd}/Pipe/test_pipe
    sim.set_folder('2D_4_')

    # load templates. It will first look in the relative directory
    # and then in the installation directory
    sim.load_template('templates/asymmetricalSplit')

    network, pipe, pipe2, pipe3, pipe4 = create_pipe(radius)
    network.create(path=sim.load_path('local'))

    sim.setup.mesher.set_blocks(network.get_blocks())
    sim.setup.mesher.set_dx(radius / 5.0)
    sim.setup.ist.add(network.get_pipes_name())

    inflow = sim.get_bc("inflow")
    inflow.set_velocities([0.25, 0.0, 0.0])
    inflow2 = sim.get_bc("inflow_liq")
    inflow2.set_velocities([0.0, -0.5, 0.0])

    tree = sim.setup.bcs.create_surfaces_tree()
    tree.get_all_surfaces().set_bc_name('wall')
    tree.get_surface_with_point(pipe.get_inlet_point()).set_bc_name('inflow')
    tree.get_surface_with_point(pipe4.get_inlet_point()).set_bc_name('inflow_liq')
    tree.get_surface_with_point(pipe2.get_outlet_point()).set_bc_name('outflow_top')
    tree.get_surface_with_point(pipe3.get_outlet_point()).set_bc_name('outflow_bot')
    tree.get_surface_with_normal('z').set_bc_name('symmetry')
    sim.setup.mesher.set_2D('x', 'y')

    sim.prepare_simulation_files()
    sim.run_init(nprocs=4)
    sim.run(nbrIterations=500, nprocs=4)
    oil = sim.setup.input.get_phase("Phase 1")
    mfr = sim.postprocess.get_mass_flow_rate("outflow_bot", oil)
    mfr = mfr/2e-7*radius
    print mfr

app.add_main(my_fun)

if __name__ == "__main__":
    inputs = app.parse_inputs()
    app.run(inputs)








