import os
from fabric.api import run, cd, local, env, put, abort
from probe.cloud import Cloud
from contextlib import contextmanager
import dataset
from terminaltables import AsciiTable

env.hosts = ['argo.physics.muni.cz']
env.warn_only = False

def sim_run(simdir='~/.simulations', sourcedir='.', cloud_cfg='cloud.cfg',
           remote_venv='probe', dbfile='~/.simulations.sqlite', 
           tmux_out_redirect='tmux.log'):

    assert cloud_cfg in os.listdir(sourcedir), 'there is no cloud config in sourcedir!'

    pwd = local('pwd', capture=True)
    print '[fab-upload] pwd: {}'.format(pwd)

    # make sure that .simulations folder exists
    run('mkdir -p {}'.format(simdir))
    with cd(simdir):
        tempdir = run('mktemp -d -p {}'.format(simdir))
        tempstr = tempdir.split('.')[-1]
        print '[fab-upload] tempdir: {}'.format(tempdir)

        put(os.path.join(sourcedir, '*'), tempdir)

        with cd(tempdir):
            with rollbackwrap(tempdir):
                run('make')

                run('tmux new -d -s {}'.format(tempstr))

                cmd_run_simulation = 'probe_cloud.py -v cloud:run_simulation'
                if tmux_out_redirect:
                    cmd_run_simulation = cmd_run_simulation + ' 2>&1 | tee {}'.format(tmux_out_redirect)
                cmd_template = 'tmux send-keys -t {}:0 "workon {} && {}" C-m'
                cmd = cmd_template.format(tempstr, remote_venv, cmd_run_simulation)

                run(cmd)

    # insert simulation into db
    db, simulations = get_db_and_simulations_table(dbfile)
    simulations.insert(dict(host=env.host_string, tempdir=tempdir, tempstr=tempstr))

    print
    print tempstr

def sim_rollback(tempstr, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    tempdir = simulations.find_one(tempstr=tempstr)['tempdir']

    print '[sim_rollback] deleting dir {}'.format(tempdir)
    run('rm -r {}'.format(tempdir))
    print '[sim_rollback] deleting record from db'
    simulations.delete(tempstr=tempstr)

def show_db(dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    if len(simulations) > 0:
        sims = [sim for sim in simulations.all()]
        sims_list = [sims[0].keys()]
        for sim in sims:
            sims_list.append([str(s) for s in sim.values()])

        table = AsciiTable(sims_list)
        print
        print 'Simulations'
        print table.table
    else:
        print 'There are no simulations in db.'
    #table = AsciiTable(simulations.all())

def show_log(tempstr, dbfile='~/.simulations.sqlite', logfile='tmux.log'):
    db, simulations = get_db_and_simulations_table(dbfile)
    tempdir = simulations.find_one(tempstr=tempstr)['tempdir']
    run('cat {}'.format(os.path.join(tempdir, logfile)))

def get_db_and_simulations_table(dbfile):
    db = dataset.connect('sqlite:///{}'.format(os.path.expanduser(dbfile)))
    simulations = db['simulations']
    return db, simulations

@contextmanager
def rollbackwrap(tempdir):
    try:
        yield
    except SystemExit:
        rollback(tempdir)
        abort("Fail!")

def rollback(tempdir):
    print '[ROLLBACK]: deleting tempdir: {}'.format(tempdir)
    run('rm -rf {}'.format(tempdir))
