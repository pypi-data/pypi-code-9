from transat.simulation import Simulation
import transat.appbuilder as appbuilder
from transat.server.server import Server
import threading
from transat.server.client import Client
import time
import os

app = appbuilder.App('Pipe')


def launch_server():
    se = Server()
    server = threading.Thread(target=se.run)
    server.daemon = True
    server.start()
    return se.get_address()


def get_postprocess_path(name):
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    return os.path.join(path, name)


def watch(url):
    cl = Client(url)
    iteration = None
    while cl.has_jobs():
        _iteration = cl.get_current_iteration()
        if iteration != _iteration:
            iteration = _iteration
            print "iteration " + str(iteration)
        time.sleep(1)

    print cl.get_current_timestep()


def get_center_line(sim):
    y = sim.setup.mesher.get_center('y')
    z = sim.setup.mesher.get_center('z')
    x1 = sim.setup.mesher.get_min('x')
    x2 = sim.setup.mesher.get_max('x')
    return [[x1, y, z], [x2, y, z]]


def my_fun(args):
    # Create a TransAT server
    url = launch_server()

    sim = Simulation("Pipe")
    # simulations is saved in {local_wd}/Pipe/test_pipe
    sim.set_folder('test_pipe', ['local'])

    # load templates. It will first look in the relative directory
    # and then in the installation directory
    sim.load_template('templates/pipe')

    # create mesh and files needed by the TransAT solver
    sim.prepare_simulation_files()

    sim.run_init(worker='local', nprocs=3, url=url)
    sim.run(worker='local', nprocs=3, url=url)

    watch(url)

    center_line = get_center_line(sim)

    sim.add_postprocess(get_postprocess_path("pipe_postprocess.py"))
    sim.run_postprocess('plot_pressure',
                        worker_name='local',
                        args={'points': center_line,
                              'folder': sim.load_path('local')})


app.add_main(my_fun)

if __name__ == '__main__':
    args = app.parse_inputs()
    app.run(args)
