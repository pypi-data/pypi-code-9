#! /usr/global/bin/python

import sys, argparse, math
from multiprocessing import Pool
import numpy as np
import nibabel as nb
from dcmstack.dcmmeta import NiftiWrapper

class const_array(object):
    def __init__(self, index_result, length=None):
        self.index_result = index_result
        self.length = length
        
    @property
    def flat(self):
        return self.__iter__()
        
    def __iter__(self):
        count = 0
        while True:
            if not self.length is None and count == self.length:
                break
            yield self.index_result
            count += 1
        
    def __getitem__(self, index):
        return self.index_result

def dce_to_r1(dce_nw, r1_0, dce_fa=None, dce_tr=None, baseline_end=1, 
              mask=None, pool=None):
    '''Convert a DCE time series to a series of R1 maps.
    
    Parameters
    ----------
    dce_nw : NiftiWrapper
        The DCE time series data
        
    r1_0 : Array or float
        The initial pre-contrast R1 value(s). Can be array with same 
        spatial shape as the DCE data, or a constant value.
        
    dce_fa : float
        The flip angle (in degrees) used to acquire the DCE data. If 
        not specified will try to get from 'dce_nw' meta data.
        
    dce_tr : float
        The repetition time (in milliseconds) used to acquire the DCE 
        data. If not specified will try to get from 'dce_nw' meta data.
        
    baseline_end : int
        The end index for the pre-contrast data in 'dce_nw'.
        
    mask : array
        Optional mask to restrict the voxels that are processed.
        
    pool : multiprocessing.Pool
        If provided, will use to do the computation in parallel
        
    Returns
    -------
    r1_series : array
        A 4D series of R1 maps.
    
    '''
    #Lookup any parameters not provided
    if dce_fa is None:
        dce_fa = dce_nw.get_meta('FlipAngle')
    if dce_tr is None:
        dce_tr = dce_nw.get_meta('RepetitionTime')
    if dce_fa is None or dce_tr is None:
        raise ValueError("Flip angle and TR image parameters not "
                         "specified or found in embedded meta data")
                         
    #Convert units
    dce_fa = math.radians(dce_fa)
    dce_tr /= 1000.
    
    #Load DCE array
    dce_data = dce_nw.nii_img.get_data()
    shape = dce_data.shape
    if len(shape) != 4:
        raise ValueError("The DCE data must be 4D")
    vol_shape = shape[:3]
    n_time = shape[3]
    
    #Handle the r1_0 input
    if isinstance(r1_0, float):
        r1_0 = const_array(r1_0)
    else:
        if r1_0.shape != vol_shape:
            raise ValueError("r1_0 must have same spatial shape as DCE data")
        r1_0 = r1_0.flat
    
    #Handle the mask data
    if mask is None:
        mask = np.ones(vol_shape, dtype=np.int8)
    elif mask.shape != vol_shape:
        raise ValueError("Mask must have same spatial shape as DCE data")
        
    #Allocate result array
    r1_series = np.zeros(shape, dtype=np.float32)
    
    #Precompute a couple of things
    sin_fa = math.sin(dce_fa)
    cos_fa = math.cos(dce_fa)
    
    #Iterate through voxels
    dce_flat = dce_data.flat
    r1_flat = r1_series.flat
    for flat_idx, mask_val in enumerate(mask.flat):
        if mask_val == 0:
            continue
        
        #Pull out values/slices we need
        start_idx = flat_idx * n_time
        end_idx = start_idx + n_time
        dce_signal = dce_flat[start_idx:end_idx]
        baseline_avg = np.mean(dce_signal[:baseline_end])
        r1_0_val = r1_0[flat_idx]
        
        #Calculate M0
        m_0 = ((baseline_avg * 
                (1. - math.exp(-dce_tr * r1_0_val) * cos_fa)) / 
               ((1. - math.exp(-dce_tr * r1_0_val)) * sin_fa)
              )
              
        if m_0 <= 0.0:
            continue
              
        #Calculate R1 values
        for time_idx, signal_val in enumerate(dce_signal):
            sig_to_m0_ratio = signal_val / m_0
            numerator = sig_to_m0_ratio - sin_fa
            denominator = (sig_to_m0_ratio * cos_fa) - sin_fa
            #If the logarithm is going to be positive or undefined, 
            #just set to zero
            if (numerator * denominator < 0 or 
               numerator / denominator > 1.0):
                continue
            r1_flat[start_idx + time_idx] = \
                (-math.log(numerator / denominator) / dce_tr)
    
    return r1_series
    
prog_descrip = """Convert DCE time series of signal intensities to 
series of R1 values.
"""

prog_epilog = """If there is embedded meta data, any unspecified flip 
angle or repetition time parameters will be looked up there."""

def main(argv=sys.argv):
    arg_parser = argparse.ArgumentParser(description=prog_descrip, 
                                         epilog=prog_epilog)
    arg_parser.add_argument('dce_nii', nargs=1, 
                            help=("4D DCE series"))
    arg_parser.add_argument('r1_0', nargs=1, 
                            help=("Constant or 3D map of R1 value(s)"))
    arg_parser.add_argument('-b', '--base-end', default=1, type=int,
                            help="End index for baseline signal")
    arg_parser.add_argument('-m', '--mask', help="Mask image")
    arg_parser.add_argument('--dce-fa', type=float, help=("Flip angle "
                            "for DCE acquisition"))
    arg_parser.add_argument('--dce-tr', type=float, 
                            help=("Repetition time for DCE acquision"))
    args = arg_parser.parse_args(argv[1:])
    
    #Load the DCE data
    dce_nw = NiftiWrapper(nb.load(args.dce_nii[0]), make_empty=True)
    
    #Setup mask
    if args.mask:
        mask = nb.load(args.mask).get_data()
    else:
        mask = None
        
    #Handle the r1_0 input
    try:
        r1_0 = float(args.r1_0[0])
    except:
        r1_0 = nb.load(args.r1_0[0]).get_data()
        
    #Compute R1 series 
    r1_series = dce_to_r1(dce_nw, r1_0, args.dce_fa, args.dce_tr, args.base_end, mask)
    
    #Write out result
    out_nii = nb.Nifti1Image(r1_series, dce_nw.nii_img.get_affine())
    nb.save(out_nii, 'r1_series.nii.gz')
    
if __name__ == "__main__":
    sys.exit(main()) 

