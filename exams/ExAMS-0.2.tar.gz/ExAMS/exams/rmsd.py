#!/usr/bin/env
'''
The exams package of the ExAMS project!!
'''

import os.path as op
import logging as log

import MDAnalysis
import MDAnalysis.analysis.align
import numpy as np
from matplotlib import pyplot as plt
from MDPlus.core import cofasu as cf

def avg_rmsd(mycofasu, uref, output='avg_rmsd_output.dat', select='all', max_snap=None):

    reps = len(mycofasu.fasulist)

    if max_snap is None:
          num_snapshots = mycofasu.fasulist[0].numframes()
    else: 
          if max_snap < mycofasu.fasulist[0].numframes():
                num_snapshots = max_snap
          else:
			    num_snapshots = mycofasu.fasulist[0].numframes()
			        	
    dat=np.empty((reps,num_snapshots))

    i = 0
    for uni in mycofasu:
        rmsd=MDAnalysis.analysis.rms.RMSD(uni.fasulist[0].u, uref, select=select,filename='rmsd{}.dat'.format(i))
        rmsd.run()
   
        if uni.fasulist[0].numframes() == num_snapshots:
            dat[i,:]=rmsd.rmsd[:,2]
        elif uni.fasulist[0].numframes() < num_snapshots:
            dat[i,:uni.fasulist[0].numframes()]=rmsd.rmsd[:,2]
            dat[i,uni.fasulist[0].numframes():num_snapshots]=np.average(rmsd.rmsd[:,2])
        else:
            dat[i,:]=rmsd.rmsd[:num_snapshots,2]			
        i = i+1	
		
    da=dat.sum(axis=0)/reps
    dat2=dat*dat
    ds=dat2.sum(axis=0)/reps
    std=np.sqrt(ds-da*da)    
    
    np.savetxt(output,np.column_stack((da,std)))
	
def rmsd_avstr(mycofasu, uref, output='rmsd_avstr_output.dat', select='all', max_snap=None):	

    refAtoms = uref.selectAtoms(select)
    ref0 = refAtoms.coordinates()
    refCoordinates = refAtoms.coordinates() - refAtoms.centerOfGeometry()
    numAtoms = len(refAtoms)
    
    reps = len(mycofasu.fasulist)
    num_snapshots = mycofasu.fasulist[0].numframes()

    if max_snap is None:
          num_snapshots = mycofasu.fasulist[0].numframes()
    else: 
          if max_snap < mycofasu.fasulist[0].numframes():
                num_snapshots = max_snap
          else:
			    num_snapshots = mycofasu.fasulist[0].numframes()

    structureAvg=np.empty((numAtoms,3))
    RMSDAvg=np.empty((num_snapshots))

    # Here, we are going to parse the trajectories of the simulations timestep by timestep.
    for k in range(num_snapshots):
          structureAvg[:,:]=0.0
          numReplicas = 0 # This variable will store the real number of replicas at our disposal.
          for i in range(reps):
                if(k<mycofasu.fasulist[i].numframes()): 
                      numReplicas += 1
                      # Before adding the coordinates up a fitting procedure is necessary in order to remove
                      # translational and rotational movement of the simulated system
                      mycofasu.fasulist[i].setfilter(select)
                      currentAtoms_coords = mycofasu.fasulist[i].coords(k)
                      structureAvg += cf.aatb(currentAtoms_coords, ref0)
          structureAvg=structureAvg/numReplicas
          RMSDAvg[k]=MDAnalysis.analysis.rms.rmsd(ref0,structureAvg)
	
    np.savetxt(output,np.column_stack((RMSDAvg,)))

def rmsd_var_avg(args):

      if args.verbosity:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
            log.info("Verbose output.")
      else:
            log.basicConfig(format="%(levelname)s: %(message)s")
      
      '''
      Input filename and topology filename are mandatory. Hence a check on 
      these two parameters should be performed:
      '''
      if (args.base_trajectory is None) or (args.name_trajectory is None) or (args.reference is None) or (args.set_size is None) or (args.max_snapshots is None):
            log.error('')
            log.error('All or any of the mandatory command line arguments is missing. Try to run the program again providing all the required inputs!')
      
      
      ref = MDAnalysis.Universe(args.reference)
      
      reps = int(args.set_size)
      
      num_snapshots = int(args.max_snapshots)+1
      
      f1 = cf.Fasu(args.reference, str(args.base_trajectory)+'0/'+str(args.name_trajectory))
      mycofasu = cf.Cofasu(f1)
      for i in range(1,reps):
		  f1 = cf.Fasu(args.reference, str(args.base_trajectory)+'{}'.format(i)+'/'+str(args.name_trajectory))
		  mycofasu.add(f1)
      
      avg_rmsd(mycofasu, ref, output=str(args.output), select='protein', max_snap=int(args.max_snapshots))

def rmsd_avg_str(args):

      if args.verbosity:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
            log.info("Verbose output.")
      else:
            log.basicConfig(format="%(levelname)s: %(message)s")

      '''
      Input filename and topology filename are mandatory. Hence a check on 
      these two parameters should be performed:
      '''
      if (args.base_trajectory is None) or (args.name_trajectory is None) or (args.reference is None) or (args.set_size is None) or (args.max_snapshots is None):
            log.error('')
            log.error('All or any of the mandatory command line arguments is missing. Try to run the program again providing all the required inputs!')

      ref = MDAnalysis.Universe(str(args.reference))
      reps=int(args.set_size)
      
      f1 = cf.Fasu(args.reference, str(args.base_trajectory)+'0/'+str(args.name_trajectory))
      mycofasu = cf.Cofasu(f1)
      
      for i in range(1,reps):
		  f1 = cf.Fasu(args.reference, str(args.base_trajectory)+'{}'.format(i)+'/'+str(args.name_trajectory))
		  mycofasu.add(f1)
      
      rmsd_avstr(mycofasu, ref, output=str(args.output), select='protein', max_snap=int(args.max_snapshots))

def rmsd_rmsd_avg_str_plot(args):

      avRmsdAndStdDev = np.genfromtxt(str(args.data1))
      avStrctRMSD = np.genfromtxt(str(args.data2))

      xValues = range(len(avStrctRMSD))
      xValues = np.array(xValues)/100.0

      fig = plt.figure(figsize=(12.777777,12.777777))
      subFig = fig.add_subplot(111)
      subFig.errorbar(xValues, avRmsdAndStdDev[:,0],  avRmsdAndStdDev[:,1], fmt='o', color='r', ecolor='b', label = "Average RMSD and variance")
      subFig.set_title("RMSD analysis",fontsize=50)
      subFig.plot(xValues, avStrctRMSD, marker='.', color='g', label = "RMSD of average structure")
      subFig.set_xlabel("Simulation time (ns)",fontsize=46)
      subFig.set_ylabel("RMSD (Angstrom)",fontsize=46)
      plt.legend(loc=8, borderaxespad=0., ncol=1, fontsize=32, bbox_to_anchor=(0.5, -0.35))
      plt.subplots_adjust(bottom=0.25)	

      for label in (subFig.get_xticklabels() + subFig.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(44)

      plt.ylim(1.2, 3.5)
      plt.show()

