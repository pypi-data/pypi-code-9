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
app.add_input("L1", unit="m")
app.add_input("L2", unit="m")
app.add_input("L3", unit="m")
app.add_input("OilVel", unit="m/s")
app.add_input("WaterVel", unit="m/s")
app.add_input("GasVel", unit="m/s")
app.add_input("Radius", unit="m")

def get_postprocess_path(name):
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    return os.path.join(path, name)

def create_pipe(L1, L2, L3, pipe_radius=0.25):
    cad = CAD(freecad_path=global_config.env['path']['freecad'])

    pipe = Pipe(name="pipe.stl", radius=pipe_radius)
    pipe.add_point([0.0, 0.0, 0])
    pipe.add_point([L1, 0.0, 0], 0.1)
    pipe.add_point([L1, L2, 0], 0.1)
    pipe.add_point([L1+L3, L2, 0])

    network = Network(cad, [pipe])

    return network, pipe

def launch_server():
    se = Server()
    server = threading.Thread(target=se.run)
    server.daemon = True
    server.start()
    return se.get_address()



def watch(url):

    widgets = ['Simulation: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
           ' ', ETA(), ' ']
    pbar = ProgressBar(widgets=widgets, maxval=100).start()

    start = time.time()
    cl = Client(url)
    iteration = None
    while cl.has_jobs():
        elapsed = (time.time() - start)
        remaining = cl.get_remaining_time()*60.0
        percentage = elapsed/(elapsed+remaining)*100
        pbar.update(percentage)
        _iteration = cl.get_current_timestep()
        if iteration != _iteration:
            iteration = _iteration
        time.sleep(1)
    pbar.finish()
    print cl.get_current_timestep()


def my_fun(inputs):
    url = launch_server()

    radius = float(inputs['Radius'])
    L1 = float(inputs['L1'])
    L2 = float(inputs['L2'])
    L3 = float(inputs['L3'])

    sim = Simulation("Severe_Slug")
    # simulations is saved in {local_wd}/Pipe/test_pipe
    sim.set_folder('2D_3', ['local'])

    # load templates. It will first look in the relative directory
    # and then in the installation directory
    sim.load_template('templates/severe_slug')

    network, pipe = create_pipe(L1, L2, L3, radius)
    network.create(path=sim.load_path('local'))

    sim.setup.mesher.set_blocks(network.get_blocks())
    sim.setup.mesher.set_dx(radius / 5.0)
    sim.setup.ist.add(network.get_pipes_name())


    gas = sim.setup.input.get_phases().get_phase("Gas")
    gas.set_density(0.71)
    oil = sim.setup.input.get_phases().get_phase("Oil")
    water = sim.setup.input.get_phases().get_phase("Water")

    sim.get_bc('inflow').set_phase_velocities(water, velocity=[float(inputs['WaterVel']), 0, 0], volume_fraction=0.2)
    sim.get_bc('inflow').set_phase_velocities(oil, velocity=[ float(inputs['OilVel']) , 0, 0], volume_fraction=0.5)
    sim.get_bc('inflow').set_phase_velocities(gas, velocity=[ float(inputs['GasVel']), 0, 0], volume_fraction=0.3)

    # is not going to chage the initial conditions. Convergence may be difficult
    sim.get_bc('outflow').set_pressure(0.0)

    tree = sim.setup.bcs.create_surfaces_tree()
    tree.get_all_surfaces().set_bc_name('wall')

    tree.get_surface_with_point(pipe.get_inlet_point()).set_bc_name('inflow')
    tree.get_surface_with_point(pipe.get_outlet_point()).set_bc_name('outflow')

    offset = 1e-7
    sim.setup.mesher.set_2D('x', 'y', offset)
    tree.get_surface_with_normal('z').set_bc_name('symmetry')

    sim.prepare_simulation_files()

    sim.run_init(worker='local', nprocs=3)
    #sim.run(worker='local', nprocs=3, url=url)
    sim.run_until(time=3, worker='local', nprocs=3, url=url)

    watch(url)

    A_2d = 2*radius*1
    A_3d = math.pi*math.pow(radius, 2)

    print sim.postprocess.get_massflow_rate_2D(sim.load_path('local'), A_2d, A_3d, [gas, water, oil], pipe.get_outlet_point(), [1,0,0])
    print sim.postprocess.get_pressure_drop(sim.load_path('local'), [0.03, 0, 0], pipe.get_outlet_point())

    print sim.load_path('local')

app.add_main(my_fun)

if __name__ == "__main__":
    inputs = app.parse_inputs()
    app.run(inputs)








