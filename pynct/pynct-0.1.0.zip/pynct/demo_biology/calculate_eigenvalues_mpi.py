"""
CALCULATION of EIGENVALUES of a given SOLUTION BRANCH  
INPUT: parameter file that contains the solution branch and info about the tissue, a file with info about the model, a name 
for a file where the eigenvalues must be saved 
OUTPUT: file with the eigenvalues 
"""

import numpy as np
import scipy as sp
import scipy.linalg as spla
from mpi4py import MPI
import time
import h5py
import pypts.tissue
import pynct.demo_biology.system.lemma_system
import pynct.demo_biology.system.reader_model
import optparse


def run_model(parameter, cont_data_file, model_info):
    """
        Calculates the eigenvalues for a given point on the branch
        parameter: point on the branch
        cont_data_file: file that contains the tissue and the branch
        model_info: info of the model
        
        returns the eigenvalues in that point
    """
    # OPEN the HDF5 storage file with continuation data 
    pynct_file = h5py.File(cont_data_file, 'r')
    
    # LOAD tissue
    t = pypts.tissue.Tissue(cont_data_file)
    
    # GET the solution point on the continuation curve
    a = pynct_file[('/step_{0}/cells_attr_IAA').format(parameter)][...]
    p = pynct_file[('/step_{0}/cells_attr_PIN').format(parameter)][...]
    u = np.concatenate((a, p),axis=0)
    
    # GET the parameters
    lambd = pynct_file['/parametervalues'][...]
    lambd[10] = pynct_file['time_steps'][parameter]
        
    #CREATE system object        
    general_f = pynct.demo_biology.system.lemma_system.lemma_system(u, lambd, t, model_info)
    
    # CALCULATE eigenvalues
    J = general_f.exactJacobian(u,lambd)
    eig_e = sp.linalg.eig(J, left = False, right=False)
    sortindex = np.argsort(eig_e.real)
    e_sort = eig_e[sortindex]

    return e_sort

def main():
    """
    Setup the calculation of the eigenvalues in all the points of the branch. Here the points are 
    distributed over the different cores.
    """
    # MPI constructs
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    
    # Check command line options
    parser = optparse.OptionParser()
    parser.add_option("-i", "--cont_data",
                  action="store",
                  type="string",
                  dest="cont_datafile",
                  help="Input file with cont_data")
    parser.add_option("-m", "--modelfile",
                  action="store",
                  type="string",
                  dest="model_file",
                  help="Input file with the model")
    parser.add_option("-o", "--out",
                  action="store",
                  type="string",
                  dest="out_file_name",
                  help="Output file name for eigenvalues")
    (options, args) = parser.parse_args()
    # if an input file is missing, ask for them and quit.
    if options.cont_datafile is None:
        print("Input file with continuation data is required, see help: -h or --help")
        exit(1)
    if options.model_file is None:
        print("Input file with the model is required, see help: -h or --help")
        exit(1)
    if options.out_file_name is None:
        print("Name for file to save eigenvalues is required, see help: -h or --help")
        exit(1)

    with open(options.model_file) as mf:
        model_info = json.load(mf)
    
    # Let the rank 0 process subdivide the workload
    if rank == 0:
        
        pynct_file = h5py.File(options.cont_datafile, 'r')
        t = pypts.tissue.Tissue(options.cont_datafile)
        
        # get value of T for every continuation step
        time_steps_T = pynct_file['time_steps'][...]

        # get number of continuation steps
        ####time_steps_idx = pynct_file['time_steps_idx'][...]
        num_steps = time_steps_T.size
        print 'het aantal bifurcatie stappen is ', num_steps
        
        # Array of parameters to run simulation for
        #parameters = np.array([0, 10, 20, 30, 40, 50])
        parameters = np.arange(num_steps)
        # Workload per process that needs to be done; i.e.: the number of parameter
        # values to be passed to each process
        workload = sp.repeat(len(parameters) / size, size)
        workload[:(len(parameters) % size)] += 1
        offset = sp.array([sp.sum(workload[:i]) for i in sp.arange(size)])
        # Array of arrays of parameter values to pass to each process
        global_params = [parameters[offset[i]:(offset[i] + workload[i])] for i in range(size)]
        # Start perf. timing
        start = time.time()
    else:
        global_params = None
        start = None

    # Distribute param values to processes
    local_params = comm.scatter(global_params, root=0)

    # Do work
    local_result = [run_model(p, options.cont_datafile, model_info) for p in local_params]

    # Gather results from all processes to the root process
    global_result = comm.gather(local_result, root=0)

    # Only the rank 0 process does the postprocessing of the results
    if rank == 0:
        result = [item for sublist in global_result for item in sublist]
        #print result
        
                  
        branch_file_name = options.out_file_name
        print 'Saving branch to: %s' % branch_file_name

        #rewrite result
        e_sort = np.zeros((2*t.getNumCells(),num_steps), complex)
        for j in range(len(result)):
            e_sort[:,j] = result[j]
        
        # Open HDF5 file for output
        out_file = h5py.File(branch_file_name, 'w')
 
        # Save the eigenvalues
        eig_data_dset = out_file.create_dataset('/eig_data', (2*t.getNumCells(),num_steps), '=c16', maxshape=(None,None), data = e_sort)



        # Clean up the hdf5 file
        out_file.close()

        #####################################################################################
        
        

    # Wait for all to finish
    comm.barrier()

    if rank == 0:
        print 'MPI time:', (time.time() - start)

if __name__ == "__main__":
    main()

