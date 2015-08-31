"""
 set of tools to plot solutions of transport systems found with continuation methods. 
"""

import optparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Slider, Button, RadioButtons
import h5py
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def chem_to_rgb(chem, min_chem, max_chem):
    relative_chem =(np.log10(chem) - np.log10(min_chem)) / (np.log10(max_chem) - np.log10(min_chem)) 
    return (1-relative_chem, relative_chem, 0)

def bifdiagram_interactive(contdata_file_name, stability=None, endpoint=None):
    """
	interactive plot of the bifurcation diagram and the corresponding solution pattern.
        the bar at the bottom indicates the current continuation step
	the stability of the solution is not shown
	INPUT: contdata_file_name: the name of the file with the continuation data, 
		   stability: default None. The name of the file with the stability data,
		   endpoint: default None: whole branch is plotted (all solution points in file) 
		   					 a value: only a part (from 0 till endpoint) of the branch is plotted. 
	OUTPUT: a plot
    """

    # Colors for nodes and edges:
    col_nodes = (0.2,0.2,1.0)
    col_edges = (0.5,0.5,1.0)

    # Open the HDF5 storage file
    contdata_file = h5py.File(contdata_file_name, 'r')

    # Time steps and time step indices
    time_steps = contdata_file['time_steps'][...]
    num_steps = time_steps.size
    logger.info('the number of continuation points in the file is %d' % num_steps)

    if endpoint == None:
    	logger.info('No number of continuation steps to plot specified, using total number')
    	endpoint = num_steps
    else:
    	logger.info('the number of points plotted on the bifurcation diagram is %d' % endpoint)
    # Loop over the steps and gather info for bifurcation diagram
    u_norms = np.zeros_like(time_steps)
    for step in xrange(num_steps):
        u = contdata_file[('/step_{0}/cells_attr_IAA').format(step)][...]
        u_norms[step] = np.linalg.norm(u)

    # stability of solutions
    if stability != None:
        stab_file = h5py.File(stability, 'r')
        stab_value = stab_file['eig_data'][...]
	if not stab_value[0,:].size ==num_steps:
		raise ValueError, 'the number of steps in the continuation file is not equal to the number of points in the stability file.'

    def update_figures(step):
        step = int(step)
        plot_tissue(step)
        plot_point(step)
        plt.draw()

    def plot_point(step):
        curr_point.set_xdata(time_steps[step])
        curr_point.set_ydata(u_norms[step])

    def plot_tissue(step):
        # Read the data for the step from HDF5
        nodes_xy = contdata_file[('/step_{0}/nodes_xy').format(step)][...]
        cells_nodes = contdata_file[('/step_{0}/cells_nodes').format(step)][...]
        cells_num_nodes = contdata_file[('/step_{0}/cells_num_nodes').format(step)][...]
        cells_attr_IAA = contdata_file[('/step_{0}/cells_attr_IAA').format(step)][...]
        time_steps = contdata_file['time_steps'][...]

        # Plot tissue:
        width_edge = 0.0
        ax_tis.cla()
        for cell_idx in np.arange(0,cells_num_nodes.size):
            cell_nodes_xy = nodes_xy[cells_nodes[cell_idx, :cells_num_nodes[cell_idx]],:2]
            cell_poly = Polygon(cell_nodes_xy,
                            facecolor=chem_to_rgb(cells_attr_IAA[cell_idx], np.min(cells_attr_IAA),
                            	                        np.max(cells_attr_IAA)), linewidth=width_edge)
            ax_tis.add_patch(cell_poly)
        ax_tis.set_aspect(1.)
    	fig.patch.set_visible(False)
    	ax_tis.axis('off')
        ax_tis.set_title('Tissue', fontsize=20)
        


    # Create the figure and subplots
    fig = plt.figure(figsize=(12, 8))
    ax_tis = fig.add_subplot(122)                          # Tissue
    ax_bif = fig.add_subplot(121)                          # Bifurcation diagram
    ax_slider = plt.axes([0.1, 0.025, 0.8, 0.025])      # Step slides
    curr_step = 0
    # Plot bifurcation diagram and the point indicating the current step
    if stability == None:
	    ax_bif.plot(time_steps[:endpoint-1], u_norms[:endpoint-1], '-')
    else:
    	# Note that this only works if the second point has the same stability prop as the first point
		stepper_begin = 1
		while stepper_begin < endpoint:
			stepper_end = stepper_begin
			while stepper_end < endpoint and np.max(np.real(stab_value[:,stepper_end]))*np.max(np.real(stab_value[:,stepper_begin])) > 0:
				stepper_end = stepper_end + 1
    		if np.max(np.real(stab_value[:,stepper_begin])) >= 0:
        		ax_bif.plot(time_steps[stepper_begin-1:stepper_end], u_norms[stepper_begin-1:stepper_end], 'k--', linewidth=2)
    		elif np.max(np.real(stab_value[:,stepper_begin])) < 0:
        		ax_bif.plot(time_steps[stepper_begin-1:stepper_end], u_norms[stepper_begin-1:stepper_end], 'k-', linewidth=2)
    		stepper_begin = stepper_end
    curr_point, = ax_bif.plot(time_steps[curr_step], u_norms[curr_step], color=(1,0,0), markersize=7, marker='o')

    # Plot the tissue in the current step
    plot_tissue(curr_step)
    # plot slider
    step_slider = Slider(ax_slider, 'Step:', 0, num_steps, valinit=curr_step)
    # update figure if slider is changed
    step_slider.on_changed(update_figures)

    # view options 
    min_node = np.zeros((num_steps,2))
    max_node = np.zeros_like(min_node)
    for step in np.arange(0,num_steps):
        nodes_xy = contdata_file[('/step_{0}/nodes_xy').format(step)][...]
        min_node[step,0] = np.min(nodes_xy[:,0])
        min_node[step,1] = np.min(nodes_xy[:,1])
        max_node[step,0] = np.max(nodes_xy[:,0])
        max_node[step,1] = np.max(nodes_xy[:,1]) 
    xmin_node = np.min(min_node[:,0])
    ymin_node = np.min(min_node[:,1])
    xmax_node = np.max(max_node[:,0])
    ymax_node = np.max(max_node[:,1])
    ax_tis.set_xlim(xmin_node-1, xmax_node+2)
    ax_tis.set_ylim(ymin_node-1,ymax_node+1)
    
    
    
    ax_bif.set_title('Bifurcation Diagram', fontsize=20)
    
    # Show the figure on screen
    plt.show()
    # Close HDF5 file
    contdata_file.close()
      





