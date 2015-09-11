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
      if (args.base_trajectory is None) or (args.name_trajectory is None) or (args.reference is None) or (args.set_size is None):
            log.error('')
            log.error('All or any of the mandatory command line arguments is missing. Try to run the program again providing all the required inputs!')
            
      ref = MDAnalysis.Universe(args.reference)
      #ref = MDAnalysis.Universe('/users/charlie/MUP2/1qy1/1qy1_g.gro')
      reps = int(args.set_size)
      #reps=100
      
      u = MDAnalysis.Universe(str(args.reference),str(args.base_trajectory)+'0/'+str(args.name_trajectory))
      
      trajlist=[]
      if args.max_snapshots is None:
            num_snapshots = u.trajectory.numframes
      else:
		    num_snapshots = int(args.max_snapshots)
      dat=np.empty((reps,num_snapshots))

      for i in range(reps):
            trajlist.append(str(args.base_trajectory)+'{}'.format(i)+'/'+str(args.name_trajectory))
            u = MDAnalysis.Universe(str(args.reference),trajlist[i])
            rmsd=MDAnalysis.analysis.rms.RMSD(u,reference=ref,select='protein',filename='rmsd{}.dat'.format(i))
            rmsd.run()
            #print trajlist[i]
            if u.trajectory.numframes == num_snapshots:
                  dat[i,:]=rmsd.rmsd[:,2]
            elif u.trajectory.numframes < num_snapshots:
		          dat[i,:u.trajectory.numframes]=rmsd.rmsd[:,2]
		          dat[i,u.trajectory.numframes:num_snapshots]=np.average(rmsd.rmsd[:,2])
            else:
                  dat[i,:]=rmsd.rmsd[:num_snapshots,2]

      #refCoordinates=ref.atoms.coordinates()
      da=dat.sum(axis=0)/reps
      dat2=dat*dat
      ds=dat2.sum(axis=0)/reps
      std=np.sqrt(ds-da*da)

      #np.savetxt('/users/ardita/DS/md5_100replicas_rmsd.dat',np.column_stack((da,std)))
      np.savetxt(str(args.output),np.column_stack((da,std)))

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
      if (args.base_trajectory is None) or (args.name_trajectory is None) or (args.reference is None) or (args.set_size is None):
            log.error('')
            log.error('All or any of the mandatory command line arguments is missing. Try to run the program again providing all the required inputs!')

      ref = MDAnalysis.Universe(str(args.reference))
      refAtoms = ref.selectAtoms("protein")
      ref0 = refAtoms.coordinates()
      refCoordinates = refAtoms.coordinates() - refAtoms.centerOfGeometry()

      reps=int(args.set_size)
      universesArray=[MDAnalysis.Universe(str(args.reference), str(args.base_trajectory)+'{}'.format(i)+'/'+str(args.name_trajectory)) for i in xrange(reps)]

      numAtoms = len(refAtoms)
      if args.max_snapshots is None:
            numFrames = universesArray[0].trajectory.numframes
      else:
		    numFrames = int(args.max_snapshots)

      structureAvg=np.empty((numAtoms,3))
      RMSDAvg=np.empty((numFrames))

      # Here, we are going to parse the trajectories of the simulations timestep by timestep.
      for k in range(numFrames):
            structureAvg[:,:]=0.0
            numReplicas = 0 # This variable will store the real number of replicas at our disposal.
            for i in range(reps):
                  if(k<universesArray[i].trajectory.numframes): # Lets postpone the task of checking the number of frames correctly.
                        numReplicas += 1
                        # Before adding the coordinates up a fitting procedure is necessary in order to remove
                        # translational and rotational movement of the simulated system
                        MDAnalysis.analysis.align.alignto(universesArray[i],ref, select="protein")
                        #localCoordinates = universesArray[i].atoms.coordinates() - universesArray[i].atoms.centerOfGeometry()
                        #R, rmsd = MDAnalysis.analysis.align.rotation_matrix(localCoordinates, refCoordinates)
                        #universesArray[i].atoms.translate(-universesArray[i].atoms.centerOfGeometry())
                        #universesArray[i].atoms.rotate(R)
                        #universesArray[i].atoms.translate(ref.atoms.centerOfGeometry())
                        currentAtoms = universesArray[i].selectAtoms("protein")
                        structureAvg += currentAtoms.coordinates()
                        # Here, at this point we should advance all universes by one timestep
                        if(k<universesArray[i].trajectory.numframes-1):
                              universesArray[i].trajectory.next()
            structureAvg=structureAvg/numReplicas
            RMSDAvg[k]=MDAnalysis.analysis.rms.rmsd(ref0,structureAvg)
	
      #np.savetxt('/users/ardita/DS/RMSDAverage3Structures.dat',np.column_stack((RMSDAvg)))
      np.savetxt(str(args.output),np.column_stack((RMSDAvg,)))


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
