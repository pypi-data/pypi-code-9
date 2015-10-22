""" Utilities for converting COLIBRI tracks into TRILEGAL tracks """
import glob
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from ast import literal_eval
from matplotlib import cm, rcParams
from matplotlib.ticker import NullFormatter, MultipleLocator, ScalarFormatter, MaxNLocator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = False
rcParams['axes.linewidth'] = 1
rcParams['ytick.labelsize'] = 'large'
rcParams['xtick.labelsize'] = 'large'
rcParams['axes.edgecolor'] = 'black'

nullfmt = NullFormatter()  # no labels

def colibri2trilegal(input_file):
    '''
    This script formats Paola's tracks and creates the files needed to use them
    with TRILEGAL as well as the option to make diagnostic plots.

    infile is an input_file object. See class InputFile

    WHAT'S GOING ON:
    Here is what it takes to go from COLIBRI agb tracks to TRILEGAL:

    1. COLIBRI tracks
    2. COLIBRI tracks formatted for TRILEGAL
    3. TRILEGAL files that link to COLIBRI re-formatted tracks

    1. COLIBRI tracks must have naming scheme
        [mix]/[set]/[Trash]_[metallicity]_[Y]/[track_identifier]
    ex: agb_caf09_z0.008/S1/agb_*Z*.dat
    ex: CAF09/S_SCS/*Z*/agb_*Z*.dat
    These can live anywhere, and do not need to be included in TRILEGAL
    directories.

    2. COLIBRI tracks are formatted for TRILEGAL with no header file.
    They only include the quiescent phases and a column with dL/dT
    (See AGBTracks)

    3. TRILEGAL needs two files to link to COLIBRI re-formatted tracks
       a. track file goes here: isotrack/tracce_[mix]_[set].dat
       b. cmd_input_file that links to the track file
          goes here trilegal_1.3/cmd_input_[mix]_[set].dat
    '''
    infile = InputFile(input_file, default_dict=agb_input_defaults())

    # set up file names and directories, cd to COLIBRI tracks.
    agb_setup(infile)

    # list of isofiles, zs, and ys to send to tracce file.
    isofiles, Zs, Ys = [], [], []
    imfr_data = np.array([])
    lifetime_data = np.array([])

    for metal_dir in infile.metal_dirs:
        metallicity, Y = metallicity_from_dir(metal_dir)
        logger.info('Z = {}'.format(metallicity))
        if infile.diag_plots is True:
            if infile.diagnostic_dir0 is not None:
                diagnostic_dir = os.path.join(infile.diagnostic_dir0, infile.agb_mix,
                                              infile.set_name, metal_dir)  + '/'
                ensure_dir(diagnostic_dir)
                # update infile class to place plots in this directory
                infile.diagnostic_dir = diagnostic_dir
            else:
                logger.error('Must specifiy diagnostic_dir0 in infile for diag plots')
                sys.exit(2)

        agb_tracks = get_files(os.path.join(infile.agbtrack_dir, infile.agb_mix,
                                            infile.set_name, metal_dir),
                               infile.track_identifier)
        agb_tracks.sort()
        assert len(agb_tracks) > 0, 'No agb tracks found!'
        iso_name_conv = '_'.join(('Z%.4f' % metallicity, infile.name_conv))
        isofile = os.path.join(infile.home, infile.isotrack_dir, iso_name_conv)


        if infile.over_write is False and os.path.isfile(isofile):
            logger.warning('not over writing {}'.format(isofile))
            out = None
        else:
            out = open(isofile, 'w')

        isofile_rel_name = os.path.join('isotrack', infile.isotrack_dir,
                                        iso_name_conv)
        logger.info('found {} tracks'.format(len(agb_tracks)))
        for i, agb_track in enumerate(agb_tracks):
            # load track
            track = get_numeric_data(agb_track)

            if track == -1:
                continue

            if track.bad_track is True:
                continue

            assert metallicity == track.metallicity, \
                'directory and track metallicity do not match'

            # make iso file for trilegal
            if out is not None:
                if i == 0:
                    make_iso_file(track, out, write_header=True)
                else:
                    make_iso_file(track, out)

            # save information for lifetime file.
            lifetime_datum = np.array([metallicity, track.mass, track.tauc,
                                       track.taum])

            lifetime_data = np.append(lifetime_data, lifetime_datum)

            # make diagnostic plots
            if infile.diag_plots is True and infile.diagnostic_dir0 is not None:
                assert metallicity_from_dir(infile.diagnostic_dir)[0] == \
                    track.metallicity, 'diag dir met wrong!'
                diag_plots(track, infile)

            # save information for imfr
            if infile.make_imfr is True:
                M_s = track.data_array['M_star']
                imfr_datum = np.array([M_s[0], M_s[-1], float(metallicity)])
                imfr_data = np.append(imfr_data, imfr_datum)

        if out is not None:
            out.close()
            logger.info('wrote {}'.format(isofile))

        # keep information for tracce file
        isofiles.append(isofile_rel_name)
        Ys.append(Y)
        Zs.append(metallicity)
        #bigplots(agb_tracks, infile)

    # make file to link cmd_input to formatted agb tracks
    make_met_file(infile.tracce_file, Zs, Ys, isofiles)

    # make cmd_input file
    cmd_in_kw = {'cmd_input_file': infile.cmd_input_file,
                 'file_tpagb': infile.tracce_file_rel,
                 'mass_loss': infile.mass_loss,
                 'file_isotrack': infile.file_isotrack}
    write_cmd_input_file(**cmd_in_kw)

    if infile.make_imfr is True and infile.diagnostic_dir0 is not None:
        ifmr_file = os.path.join(infile.diagnostic_dir0, infile.agb_mix,
                                 infile.set_name,
                                 '_'.join(('ifmr', infile.name_conv)))
        ncols = 3
        nrows = imfr_data.size/ncols
        savetxt(ifmr_file, imfr_data.reshape(nrows, ncols),
                       header='# M_i M_f Z \n')
        plot_ifmr(ifmr_file)

    if infile.diagnostic_dir0 is not None and infile.diag_plots is True:
        lifetime_file = os.path.join(infile.diagnostic_dir0, infile.agb_mix,
                                     infile.set_name,
                                     '_'.join(('tau_cm', infile.name_conv)))
        ncols = 4
        nrows = lifetime_data.size / ncols
        savetxt(lifetime_file, lifetime_data.reshape(nrows, ncols),
                       header='# z mass tauc taum\n')
        plot_cluster_test(lifetime_file)

    os.chdir(infile.home)
    return infile.cmd_input_file


def agb_setup(infile):
    '''set up files and directories for TPAGB parsing.'''
    infile.home = os.getcwd()

    # Check for Paola's formatted tracks
    ensure_dir(infile.isotrack_dir)

    # are we making diagnostic plots, check directory.
    if infile.diagnostic_dir0:
        ensure_dir(os.path.join(infile.diagnostic_dir0, infile.agb_mix,
                                       infile.set_name + '/'))
    else:
        logger.info('not making diagnostic plots')

    # set name convention: [mix]_[set].dat
    infile.name_conv = '{}_{}.dat'.format(infile.agb_mix, infile.set_name)

    # set track search string
    infile.track_identifier = 'agb_*Z*.dat'

    # cmd_input_file that links to the track file
    cmd_input = '_'.join(('cmd', 'input', infile.name_conv))
    ensure_dir(os.path.join(infile.home, infile.trilegal_dir))
    infile.cmd_input_file = os.path.join(infile.home, infile.trilegal_dir,
                                         cmd_input)

    # track file to link from cmd_input to paola's formatted tracks
    tracce_fh = '_'.join(('tracce', infile.name_conv))

    infile.tracce_file = os.path.join(infile.home, infile.tracce_dir,
                                      tracce_fh)

    infile.tracce_file_rel = os.path.join('isotrack', infile.tracce_dir,
                                          tracce_fh)

    # moving to the the directory with metallicities.
    infile.working_dir = os.path.join(infile.agbtrack_dir, infile.agb_mix,
                                      infile.set_name)
    os.chdir(infile.working_dir)
    metal_dirs = [m for m in os.listdir(infile.working_dir)
                  if os.path.isdir(m) and 'Z' in m]

    if infile.metals_subset is not None:
        logger.info('doing a subset of metallicities')
        metal_dirs = [m for m in metal_dirs
                      if metallicity_from_dir(m)[0] in infile.metals_subset]
    metals = np.argsort([metallicity_from_dir(m)[0] for m in metal_dirs])
    infile.metal_dirs = np.array(metal_dirs)[metals]
    logger.info('found {} metallicities'.format(len(infile.metal_dirs)))


def metallicity_from_dir(met):
    ''' take Z and Y values from string'''
    if met.endswith('/'):
        met = met[:-1]

    if len(os.path.split(met)) > 0:
        met = os.path.split(met)[1]

    z = float(met.split('_')[1].replace('Z', ''))
    y = float(met.split('_')[-1].replace('Y', ''))

    return z, y


class AGBTracks(object):
    '''AGB data class'''
    def __init__(self, data_array, col_keys, name):
        self.data_array = data_array
        self.key_dict = dict(zip(col_keys, range(len(col_keys))))
        self.name = name
        self.firstname = os.path.split(name)[1]
        self.mass = float(self.firstname.split('_')[1])
        self.metallicity = float(self.firstname.split('_')[2].replace('Z', ''))
        # initialize: it's a well formatted track with more than one pulse
        self.bad_track = False
        # if only one thermal pulse, stop the press.
        self.check_ntp()
        self.get_TP_inds()
        if not self.bad_track:
            # force the beginning phase to not look like it's quiescent
            self.fix_phi()
            # load quiescent tracks
            self.get_quiescent_inds()
            # load indices of m and c stars
            self.m_cstars()
            # calculate the lifetimes of m and c stars
            self.tauc_m()
            # add points to low mass quiescent track for better interpolation
            self.addpt = []
            if len(self.Qs) <= 9 and self.mass < 3.:
                self.add_points_to_q_track()
            # find dl/dt of track
            self.find_dldt()
        else:
            logger.error('bad track: {}'.format(name))

    def find_dldt(self, order=1):
        '''
        Finds dL/dt of track object by a poly fit of order = 1 (default)
        '''
        TPs = self.TPs
        qs = list(self.Qs)
        status = self.data_array['status']
        logl = self.data_array['L_star']
        logt = self.data_array['T_star']
        phi = self.data_array['PHI_TP']
        # if a low mass interpolation point was added it will get
        # the same slope as the rest of the thermal pulse.
        #dl/dT seems somewhat linear for 0.2 < phi < 0.4 ...
        lin_rise, = np.nonzero((status == 7) & (phi < 0.4) & (phi > 0.2))
        rising = [list(set(TP) & set(lin_rise)) for TP in TPs]
        fits = [np.polyfit(logt[r], logl[r], order) for r in rising if len(r) > 0]
        slopes = np.array([])
        # first line slope
        slopes = np.append(slopes, (logl[2] - logl[0]) / (logt[2] - logt[0]))
        # poly fitted slopes
        slopes = np.append(slopes, [fits[i][0] for i in range(len(fits))])

        # pop in an additional copy of the slope if an interpolation point
        # was added.
        if len(self.addpt) > 0:
            tps_of_addpt = np.array([i for i in range(len(TPs))
                                    if list(set(self.addpt) & set(TPs[i])) > 0])
            slopes = np.insert(slopes, tps_of_addpt, slopes[tps_of_addpt])

        self.Qs = np.insert(self.Qs, 0, 0)
        self.rising = rising
        self.slopes = slopes
        self.fits = fits

    def add_points_to_q_track(self):
        '''
        when to add an extra point for low masses
        if logt[qs+1] is hotter than logt[qs]
        and there is a point inbetween logt[qs] and logt[qs+1] that is cooler
        than logt[qs] add the coolest point.
        '''
        addpt = self.addpt
        qs = list(self.Qs)
        logt = self.data_array['T_star']
        tstep = self.data_array['step']
        status = self.data_array['status']
        Tqs = logt[qs]
        # need to use some unique array, not logt, since logt could repeat,
        # index would find the first one, not necessarily the correct one.
        Sqs = tstep[qs] - 1.  # steps start at 1, not zero
        # takes the sign of the difference in logt(qs)
        # if the sign of the difference is more than 0, we're going from cold to ho

        # finds where the logt goes from getting colder to hotter...
        ht, = np.nonzero(np.sign(np.diff(Tqs)) > 0)
        ht = np.append(ht, ht + 1)  # between the first and second
        Sqs_ht = Sqs[ht]
        # the indices between each hot point.
        t_mids = [map(int, tstep[int(Sqs_ht[i]): int(Sqs_ht[i + 1])])
                  for i in range(len(Sqs_ht) - 1)]
        Sqs_ht = Sqs_ht[: -1]
        for i in range(len(Sqs_ht) - 1):
            hot_inds = np.nonzero(logt[int(Sqs_ht[i])] > logt[t_mids[i]])[0]
            if len(hot_inds) > 0:
                # index of the min T of the hot index from above.
                addpt.append(list(logt).index(np.min(logt[[t_mids[i][hi]
                                                           for hi in hot_inds]])))

        if len(addpt) > 0:
            addpt = np.unique([a for a in addpt if status[a] == 7.])
        # hack: if there is more than one point, take the most evolved.
        if len(addpt) > 1:
            addpt = [np.max(addpt)]
        # update Qs with added pts.
        self.Qs = np.sort(np.concatenate((addpt, qs)))
        self.addpt = addpt

    def check_ntp(self):
        '''sets self.bad_track = True if only one thermal pulse.'''
        ntp = self.data_array['NTP']
        if ntp.size == 1:
            logger.error('no tracks! {}'.format(self.name))
            self.bad_track = True

    def fix_phi(self):
        '''The first line in the agb track is 1. This isn't a quiescent stage.'''
        self.data_array['PHI_TP'][0] = -1.

    def m_cstars(self, mdot_cond=-5, logl_cond=3.3):
        '''
        adds mstar and cstar attribute of indices that are true for:
        mstar: co <=1 logl >= 3.3 mdot <= -5
        cstar: co >=1 mdot <= -5
        (by default) adjust mdot with mdot_cond and logl with logl_cond.
        '''
        data = self.data_array

        self.mstar, = np.nonzero((data['CO'] <= 1) &
                                 (data['L_star'] >= logl_cond) &
                                 (data['dMdt'] <= mdot_cond))
        self.cstar, = np.nonzero((data['CO'] >= 1) &
                                 (data['dMdt'] <= mdot_cond))

    def tauc_m(self):
        '''lifetimes of c and m stars'''
        try:
            tauc = np.sum(self.data_array['dt'][self.cstar]) / 1e6
        except IndexError:
            tauc = 0.
            logger.warning('no tauc')
        try:
            taum = np.sum(self.data_array['dt'][self.mstar]) / 1e6
        except IndexError:
            taum = 0.
            logger.warning('no taum')
        self.taum = taum
        self.tauc = tauc

    def get_TP_inds(self):
        '''find the thermal pulsations of each file'''
        self.TPs = []
        if self.bad_track:
            return
        ntp = self.data_array['NTP']
        un, iTPs = np.unique(ntp, return_index=True)
        if un.size == 1:
            logger.warning('only one themal pulse.')
            self.TPs = un
        else:
            # The indices each TP is just filling values between the iTPs
            # and the final grid point
            iTPs = np.append(iTPs, len(ntp))
            self.TPs = [np.arange(iTPs[i], iTPs[i+1])
                        for i in range(len(iTPs) - 1)]

        if len(self.TPs) == 1:
            self.bad_track = True

    def get_quiescent_inds(self):
        '''
        The quiescent phase, Qs,  is the the max phase in each TP,
        i.e., closest to 1.
        '''
        phi = self.data_array['PHI_TP']
        logl = self.data_array['L_star']
        self.Qs = np.unique([TP[np.argmax(phi[TP])] for TP in self.TPs])
        self.mins = np.unique([TP[np.argmin(logl[TP])] for TP in self.TPs])


def get_numeric_data(filename):
    '''
    made to read all of Paola's tracks. It takes away her "lg" meaning log.
    Returns an AGBTracks object. If there is a problem reading the data, all
    data are passed as zeros.
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    line = lines[0]
    if len(lines) == 1:
        logger.warning('only one line in {}'.format(filename))
        return -1
    col_keys = line.replace('#', '').replace('lg', '').replace('*', 'star')
    col_keys = col_keys.strip().split()
    try:
        data = np.genfromtxt(filename, missing_values='************',
                             names=col_keys)
    except ValueError:
        logger.error('problem with', filename)
        data = np.zeros(len(col_keys))
    return AGBTracks(data, col_keys, filename)


def calc_c_o(row):
    """
    C or O excess
    if (C/O>1):
        excess = log10 [(YC/YH) - (YO/YH)] + 12
    if C/O<1:
        excess = log10 [(YO/YH) - (YC/YH)] + 12

    where YC = X(C12)/12 + X(C13)/13
          YO = X(O16)/16 + X(O17)/17 + X(O18)/18
          YH = XH/1.00794
    """
    yh = row['H'] / 1.00794
    yc = row['C12'] / 12. + row['C13'] / 13.
    yo = row['O16'] / 16. + row['O17'] / 17. + row['O18'] / 18.

    if row['CO'] > 1:
        excess = np.log10((yc / yh) - (yo / yh)) + 12.
    else:
        excess = np.log10((yo / yh) - (yc / yh)) + 12.

    return excess


def make_iso_file(track, isofile, write_header=False):
    '''
    this only writes the quiescent lines and the first line.
    format of this file is:
    age : age in yr
    logl : logL
    logte : logTe
    mass : actual mass along track
    mcore : core mass
    per : period in days
    period mode : 1=first overtone, 0=fundamental mode
    mlr : mass loss rate in Msun/yr
    x_min : X
    y_min : Y
    X_C : X_C
    X_N : X_N
    X_O : X_O
    slope : dTe/dL
    X_Cm : X_C at log L min of (the following) TP
    X_Nm : X_N at log L min of (the following) TP
    X_Om : X_O at log L min of (the following) TP
    '''
    isofile.write('# age(yr) logL logTe m_act mcore period ip')
    isofile.write(' Mdot(Msun/yr) X Y X_C X_N X_O dlogTe/dlogL X_Cm X_Nm X_Om\n')

    fmt = '%.4e %.4f %.4f %.5f %.5f %.4e %i %.4e %.6e %.6e %.6e %.6e %.6e %.4f  %.6e %.6e %.6e\n'

    # cull agb track to quiescent
    rows = track.Qs
    # min of each TP
    mins = track.mins

    keys = track.key_dict.keys()
    vals = track.key_dict.values()
    col_keys = np.array(keys)[np.argsort(vals)]

    #cno = [key for key in col_keys if (key.startswith('C1') or
    #                                   key.startswith('N1') or
    #                                   key.startswith('O1'))]

    isofile.write(' %.4f %i # %s \n' % (track.mass, len(rows), track.firstname))

    for i, r in enumerate(rows):
        row = track.data_array[r]
        mdot = 10 ** (row['dMdt'])
        # CNO and excess are no longer used
        #CNO = np.sum([row[c] for c in cno])
        #excess = calc_c_o(row)
        xc = np.sum([row[c] for c in col_keys if c.startswith('C1')])
        xn = np.sum([row[c] for c in col_keys if c.startswith('N1')])
        xo = np.sum([row[c] for c in col_keys if c.startswith('O1')])

        xcm = np.sum([track.data_array[mins][c] for c in col_keys if c.startswith('C1')])
        xnm = np.sum([track.data_array[mins][c] for c in col_keys if c.startswith('N1')])
        xom = np.sum([track.data_array[mins][c] for c in col_keys if c.startswith('O1')])

        period = row['P1']
        if row['Pmod'] == 0:
            period = row['P0']

        if r == rows[-1]:
            # adding nonsense slope for the final row.
            slope = 999
            xcm = 999
            xnm = 999
            xom = 999
        else:
            try:
                slope = 1. / track.slopes[list(rows).index(r)]
            except:
                logger.error('bad slope: {}, row: {}'.format(track.firstname, i))
        try:
            isofile.write(fmt % (row['ageyr'], row['L_star'], row['T_star'],
                                 row['M_star'], row['M_c'], period, row['Pmod'],
                                 mdot, row['H'], row['Y'],
                                 xc, xn, xo, slope, xcm, xnm, xom))
        except IndexError:
            logger.error('this row: {}'.format(list(rows).index(r)))
            logger.error('row length: {} slope array length {}'.format(len(rows), len(track.slopes)))
            logger.error('slope reciprical: {}'.format(1. / slope[list(rows).index(r)]))
    return


class InputFile(object):
    '''
    a class to replace too many kwargs from the input file.
    does two things:
    1. sets a default dictionary (see input_defaults) as attributes
    2. unpacks the dictionary from load_input as attributes
        (overwrites defaults).
    '''
    def __init__(self, filename, default_dict=None):
        if default_dict is not None:
            self.set_defaults(default_dict)
        self.in_dict = load_input(filename)
        self.unpack_dict()

    def set_defaults(self, in_def):
        self.unpack_dict(udict=in_def)

    def unpack_dict(self, udict=None):
        if udict is None:
            udict = self.in_dict
        [self.__setattr__(k, v) for k, v in udict.items()]


def load_input(filename, comment_char='#', list_sep=','):
    '''
    read an input file into a dictionary

    Ignores all lines that start with #
    each line in the file has format key  value
    True and False are interpreted as bool
    converts values to float, string, or list
    also accepts dictionary with one key and one val
        e.g: inp_dict      {'key': val1}

    Parameters
    ----------
    filename : string
        filename to parse
    comment_char : string
        skip line if it starts with comment_char
    list_sep : string
        within a value, if it's a list, split it by this value
        if it's numeric, it will make a np.array of floats.
    Returns
    -------
    d : dict
        parsed information from filename
    '''
    d = {}
    with open(filename) as f:
        # skip comment_char, empty lines, strip out []
        lines = [l.strip().translate(None, '[]') for l in f.readlines()
                 if not l.startswith(comment_char) and len(l.strip()) > 0]

    # fill the dict
    for line in lines:
        key, val = line.partition(' ')[0::2]
        d[key] = is_numeric(val.replace(' ', ''))

    # check the values
    for key in d.keys():
        # is_numeric already got the floats and ints
        if type(d[key]) == float or type(d[key]) == int:
            continue
        # check for a comma separated list
        temp = d[key].split(list_sep)
        if len(temp) > 1:
            try:
                # assume list of floats.
                d[key] = [is_numeric(t) for t in temp]
            except:
                d[key] = temp
        # check for a dictionary
        elif len(d[key].split(':')) > 1:
            temp1 = d[key].split(':')
            d[key] = {is_numeric(temp1[0]): is_numeric(temp1[1])}
        else:
            val = temp[0]
            # check bool
            true = val.upper().startswith('TRUE')
            false = val.upper().startswith('FALSE')
            none =  val.title().startswith('None')
            if true or false or none:
                val = literal_eval(val)
            d[key] = val
    return d


def agb_input_defaults(profile=None):
    '''

# COLIBRI directory structure must be [agbtrack_dir]/[agb_mix]/[set_name]
agbtrack_dir    /home/rosenfield/research/TP-AGBcalib/AGBTracks
agb_mix         CAF09
set_name        S_NOV13

### Parameters for TRILEGAL INPUT:

# Where input files will go for TRILEGAL
trilegal_dir    cmd_inputfiles/

# Non-TP-AGB tracks to use
file_isotrack             isotrack/parsec/CAF09_V1.2S_M36_S12D_NS_NAS.dat

# mass_loss parameter (for RGB stars) so far only "Reimers: [float]"
mass_loss       Reimers: 0.2

# TRILEGAL formatted TP-AGB tracks will go here:
# structure: [isotrack_dir]/[agb_mix]/[set_name]
isotrack_dir    isotrack_agb/

# File to link TRILEGAL formatted TP-AGB tracks to cmd_input:
tracce_dir      isotrack_agb/

### Diag plots, extra files:

# make initial and final mass relation (and also lifetimes c and m)?
# (Need more than one metallicity)
make_imfr       True

# Diagnostic plots base, this will have directory structure:
# diagnostic_dir/[agb_mix]_[metallicity]/[set]/
diagnostic_dir0            /home/rosenfield/research/TP-AGBcalib/diagnostics/

# If True, will make HRD or age vs C/O, log L, log Te (takes time!)
diag_plots  True

### Misc Options:

# overwrite TRILEGAL formatted TP-AGB tracks and the output diag plots?
over_write   True

# only do these metallicities (if commented out, do all metallicities)
# NB: this functionality has not been tested recently
#metals_subset       0.001, 0.004, 0.0005, 0.006, 0.008, 0.01, 0.017
    '''
    if profile is None:
        keys = ['over_write',
                'agbtrack_dir',
                'agb_mix',
                'set_name',
                'trilegal_dir',
                'isotrack_dir',
                'tracce_dir',
                'diagnostic_dir0',
                'make_imfr',
                'mass_loss',
                'metals_subset']
    else:
        logger.error('only default profile set... must code')

    in_def = {}
    for k in keys:
        in_def[k] = None
    return in_def


def write_cmd_input_file(**kwargs):
    '''
    make a TRILEGAL cmd_input file based on default.

    Send each parameter that is different than default by:
    kwargs = { 'kind_tpagb': 4, 'file_tpagb': 'isotrack/tracce_CAF09_S0.dat'}
    cmd_input_file = write_cmd_input_file(**kwargs)

    To make the default file:
    cmd_input_file = write_cmd_input_file()

    if you don't specify cmd_input_file, output goes to cmd_input_TEMP.dat
    '''
    kind_tracks = kwargs.get('kind_tracks', 2)
    file_isotrack = kwargs.get('file_isotrack', 'isotrack/parsec/CAF09.dat')
    file_lowzams = kwargs.get('file_lowzams', 'isotrack/bassazams_fasulla.dat')
    kind_tpagb = kwargs.get('kind_tpagb', 4)
    file_tpagb = kwargs.get('file_tpagb')
    if not file_tpagb:
        file_tpagb = 'isotrack/isotrack_agb/tracce_CAF09_AFEP02_I1_S1.dat'

    kind_postagb = kwargs.get('kind_postagb', 0)
    file_postagb = kwargs.get('file_postagb', 'isotrack/final/pne_wd_test.dat')
    mass_loss = kwargs.get('mass_loss')
    if mass_loss:
        kind_rgbmloss = 1
        law_mass_loss, = mass_loss.keys()
        efficiency_mass_loss, = mass_loss.values()
    # these are for using cmd2.2:
    kind_mag = kwargs.get('kind_mag', None)
    photsys = kwargs.get('photsys', 'wfpc2')
    file_mag = 'tab_mag_odfnew/tab_mag_%s.dat' % photsys
    kind_imf = kwargs.get('kind_imf', None)
    file_imf = kwargs.get('file_imf', 'tab_imf/imf_chabrier_lognormal.dat')

    # if not using cmd2.2:
    if kind_imf is None:
        kind_imfr = kwargs.get('kind_imfr', 0)
        file_imfr = kwargs.get('file_imfr', 'tab_ifmr/weidemann.dat')

    track_comments = '# kind_tracks, file_isotrack, file_lowzams'
    tpagb_comments = '# kind_tpagb, file_tpagb'
    pagb_comments = '# kind_postagb, file_postagb DA VERIFICARE file_postagb'
    mag_comments = '# kind_mag, file_mag'
    imf_comments = '# kind_imf, file_imf'
    imfr_comments = '# ifmr_kind, file with ifmr'
    mass_loss_comments = '# RGB mass loss: kind_rgbmloss, law, and efficiency'
    footer = (
        '################################explanation######################',
        'kind_tracks: 1= normal file',
        'file_isotrack: tracks for low+int mass',
        'file_lowzams: tracks for low-ZAMS',
        'kind_tpagb:',
        ' 0 = none',
        ' 1 = Girardi et al., synthetic on the flight, no dredge up',
        ' 2 = Marigo & Girardi 2001, from file, includes mcore and C/O',
        ' 3 = Marigo & Girardi 2007, from file, includes per, mode and mloss',
        ' 4 = Marigo et al. 2011, from file, includes slope',
        'file_tpagb: tracks for TP-AGB',
        'kind_postagb:',
        ' 0 = none',
        ' 1 = from file',
        'file_postagb: PN+WD tracks',
        'kind_ifmr:',
        ' 0 = default',
        ' 1 = from file\n')
    cmd_input_file = kwargs.get('cmd_input_file', 'cmd_input_TEMP.dat')
    fh = open(cmd_input_file, 'w')
    formatter = ' %i %s %s \n'
    fh.write(' %i %s %s %s \n' % (kind_tracks, file_isotrack, file_lowzams,
                                  track_comments))
    fh.write(formatter % (kind_tpagb, file_tpagb, tpagb_comments))
    fh.write(formatter % (kind_postagb, file_postagb, pagb_comments))
    if kind_mag is not None:
        fh.write(formatter % (kind_mag, file_mag, mag_comments))
    if kind_imf is None:
        fh.write(formatter % (kind_imfr, file_imfr, imfr_comments))
    else:
        fh.write(formatter % (kind_imf, file_imf, imf_comments))
    if mass_loss:
        fh.write(' %i %s %.3f \n' % (kind_rgbmloss, law_mass_loss,
                                     efficiency_mass_loss))
    fh.write('\n'.join(footer))
    fh.close()
    logger.info('wrote {}'.format(cmd_input_file))
    return cmd_input_file


def make_met_file(tracce, Zs, Ys, isofiles):
    with open(tracce, 'w') as t:
        t.write(' %i\n' % len(isofiles))
        [t.write(' %.4f\t%.3f\t%s\n' % (Zs[i], Ys[i], isofiles[i]))
         for i in np.argsort(Zs)]
    logger.info('wrote {}'.format(tracce))
    return


def get_files(src, search_string):
    '''
    returns a list of files, similar to ls src/search_string
    '''
    if not src.endswith('/'):
        src += '/'
    try:
        files = glob.glob1(src, search_string)
    except IndexError:
        logging.error('Can''t find %s in %s' % (search_string, src))
        sys.exit(2)
    files = [os.path.join(src, f)
             for f in files if ensure_file(os.path.join(src, f), mad=False)]
    return files


def ensure_file(f, mad=True):
    '''
    Parameters
    ----------
    f : string
        if f is not a file will log warning.
    mad : bool [True]
        if mad is True, will exit if f is not a file
    '''
    test = os.path.isfile(f)
    if test is False:
        logging.warning('there is no file', f)
        if mad:
            sys.exit(2)
    return test


def load_input(filename):
    '''
    reads an input file into a dictionary.
    file must have key first then value(s)
    Will make 'True' into a boolean True
    Will understand if a value is a float, string, or list, etc.
    Ignores all lines that start with #, but not with # on the same line as
    key, value.
    '''
    try:
        literal_eval
    except NameError:
        from ast import literal_eval

    d = {}
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            if len(line.strip()) == 0:
                continue
            key, val = line.strip().partition(' ')[0::2]
            d[key] = is_numeric(val.replace(' ', ''))
    # do we have a list?
    for key in d.keys():
        # float
        if type(d[key]) == float:
            continue
        # list:
        temp = d[key].split(',')
        if len(temp) > 1:
            try:
                d[key] = map(float, temp)
            except:
                d[key] = temp
        # dict:
        elif len(d[key].split(':')) > 1:
            temp1 = d[key].split(':')
            d[key] = {is_numeric(temp1[0]): is_numeric(temp1[1])}
        else:
            val = temp[0]
            # boolean
            true = val.upper().startswith('TR')
            false = val.upper().startswith('FA')
            if true or false:
                val = literal_eval(val)
            # string
            d[key] = val
    return d


def ensure_dir(f):
    '''
    will make all dirs necessary for input to be an existing directory.
    if input does not end with '/' it will add it, and then make a directory.
    '''
    if not f.endswith('/'):
        f += '/'

    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)
        logging.info('made dirs: {}'.format(d))


def savetxt(filename, data, fmt='%.4f', header=None):
    '''
    np.savetxt wrapper that adds header. Some versions of savetxt
    already allow this...
    '''
    with open(filename, 'w') as f:
        if header is not None:
            f.write(header)
        np.savetxt(f, data, fmt=fmt)
    logger.info('wrote {}'.format(filename))


def is_numeric(lit):
    """
    value of numeric: literal, string, int, float, hex, binary
    From http://rosettacode.org/wiki/Determine_if_a_string_is_numeric#Python
    """
    # Empty String
    if len(lit) <= 0:
        return lit
    # Handle '0'
    if lit == '0':
        return 0
    # Hex/Binary
    if len(lit) > 1:  # sometimes just '-' means no data...
        litneg = lit[1:] if lit[0] == '-' else lit
        if litneg[0] == '0':
            if litneg[1] in 'xX':
                return int(lit, 16)
            elif litneg[1] in 'bB':
                return int(lit, 2)
            else:
                try:
                    return int(lit, 8)
                except ValueError:
                    pass
    # Int/Float/Complex
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    try:
        return complex(lit)
    except ValueError:
        pass
    return lit


def setup_multiplot(nplots, xlabel=None, ylabel=None, title=None,
                    subplots_kwargs={}):
    '''
    fyi subplots args:
        nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
        subplot_kw=None, **fig_kw
    '''
    nx = np.round(np.sqrt(nplots))
    nextra = nplots - nx ** 2
    ny = nx
    if nextra > 0:
        ny += 1
    nx = int(nx)
    ny = int(ny)

    (fig, axs) = plt.subplots(nrows=nx, ncols=ny, **subplots_kwargs)
    if ylabel is not None:
        axs[0][0].annotate(ylabel, fontsize=45, xy=(0.04, 0.5),
                         xycoords='figure fraction', va='center',
                         rotation='vertical')
    if xlabel is not None:
        axs[0][0].annotate(xlabel, fontsize=45, xy=(0.5, 0.04),
                         xycoords='figure fraction', va='center')
    if title is not None:
        axs[0][0].annotate(title, fontsize=45, xy=(0.5, 1. - 0.04),
                         xycoords='figure fraction', va='center')

    return (fig, axs)


def discrete_colors(ncolors, colormap='gist_rainbow'):
    colors = []
    cmap = cm.get_cmap(colormap)
    # color will now be an RGBA tuple
    colors = [(cmap(1. * i / ncolors)) for i in range(ncolors)]
    return colors


def two_panel_plot_vert(fign=2):
    fig = plt.figure(fign, figsize=(8, 8))
    left, width = 0.13, 0.83
    bottom, height = 0.1, 0.41
    dh = 0.03

    axis1 = [left, bottom, width, height]
    axis2 = [left, (bottom + height + dh), width, height]

    ax1 = plt.axes(axis1)
    ax2 = plt.axes(axis2)
    ax2.xaxis.set_major_formatter(nullfmt)
    return ax1, ax2


def diag_plots(track, infile, plot_slopes=False):
    agb_mix = infile.agb_mix
    set_name = infile.set_name
    ext = '.png'
    logt_lim = (3.75, 3.35)
    logl_lim = (2.4, 4.8)
    lage_lim = (1., 1e7)
    co_lim = (0, 5)

    logl = track.data_array['L_star']
    logt = track.data_array['T_star']
    addpt = track.addpt
    Qs = list(track.Qs)
    # HRD
    fig = plt.figure()
    ax = plt.axes()
    plotpath = os.path.join(infile.diagnostic_dir, 'HRD/')
    ensure_dir(plotpath)
    ax.annotate(r'$%s$' % agb_mix.replace('_', '\ '), xy=(3.43, 2.8))
    ax.annotate(r'$%s$' % set_name.replace('_', '\ '), xy=(3.43, 2.7))
    ax.annotate(r'$M=%.2f$' % track.mass, xy=(3.43, 2.6))
    ax.plot(logt, logl, color='black')

    ax.plot(logt[Qs], logl[Qs], color='green', lw=2)
    ax.plot(logt[Qs], logl[Qs], 'o', color='green')
    if len(addpt) > 0:
        ax.plot(logt[addpt], logl[addpt], 'o', color='purple')
    if plot_slopes:
        hrd_slopes(track, ax)
    ax.set_xlim(logt_lim)
    ax.set_ylim(logl_lim)
    ax.set_xlabel(r'$\log\ Te$')
    ax.set_ylabel(r'$\log\ L_{\odot}$')
    fname = os.path.split(track.name)[1].replace('.dat', '')
    fig_name = os.path.join(plotpath, '_'.join(('diag', fname)))
    plt.savefig('%s%s' % (fig_name, ext))
    plt.close()

    fig, (axs) = plt.subplots(nrows=4)
    ycols = ['logl', 'logt', 'C/O', 'excess']
    annotate = [False, False, False, True]
    save_plot = [False, False, False, True]
    xlabels = [False, False, False, True]
    for i in range(len(ycols)):
        age_vs_plot(track, infile, ycol=ycols[i], ax=axs[i], annotate=annotate[i],
                    xlabels=xlabels[i], ylabels=True, save_plot=save_plot[i])


def age_vs_plot(track, infile, ycol='logl', ax=None, annotate=True, xlabels=True,
                save_plot=True, ylabels=True):
    #import pdb; pdb.set_trace()
    agb_mix = infile.agb_mix
    set_name = infile.set_name

    if ycol == 'logl':
        ydata= track.data_array['L_star']
        majL = MultipleLocator(.2)
        minL = MultipleLocator(.1)
        ylab = '$\log\ L_{\odot}$'
    elif ycol == 'logt':
        ydata = track.data_array['T_star']
        majL = MultipleLocator(.1)
        minL = MultipleLocator(.05)
        ylab = '$\log\ Te$'
    elif ycol == 'C/O':
        ydata = track.data_array['CO']
        majL = MaxNLocator(4)
        minL = MaxNLocator(2)
        ylab = '$C/O$'
    elif ycol == 'excess':
        ydata = np.array([calc_c_o(track.data_array[i])
                          for i in range(len(track.data_array))])
        majL = MaxNLocator(4)
        minL = MaxNLocator(2)
        ylab = '$Excess$'
    else:
        logger.error('logl, logt, C/O only choices for y.')
        return

    age = track.data_array['ageyr']
    addpt = track.addpt
    Qs = list(track.Qs)

    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(age, ydata, color='black')
    ax.plot(age[Qs], ydata[Qs], 'o', color='green')

    if len(addpt) > 0:
        ax.plot(age[addpt], ydata[addpt], 'o', color='purple')
    ax.yaxis.set_major_locator(majL)
    ax.yaxis.set_minor_locator(minL)
    majorFormatter = ScalarFormatter()
    majorFormatter.set_powerlimits((-3, 4))
    ax.xaxis.set_major_formatter(majorFormatter)

    if annotate:
        ax.text(0.06, 0.87, '${\\rm %s}$' % agb_mix.replace('_', '\ '),
                transform=ax.transAxes)
        ax.text(0.06, 0.77,'${\\rm %s}$' % set_name.replace('_', '\ '),
                transform=ax.transAxes)
        ax.text(0.06, 0.67, '$M=%.2f$' % track.mass,
                transform=ax.transAxes)
    if ylabels:
        ax.set_ylabel('$%s$' % ylab, fontsize=20)
    if xlabels:
        ax.set_xlabel('$\rm{Age (yr)}$', fontsize=20)

    if save_plot:
        plotpath = os.path.join(infile.diagnostic_dir, 'age_v/')
        ensure_dir(plotpath)
        fname = os.path.split(track.name)[1].replace('.dat', '')
        fig_name = os.path.join(plotpath, '_'.join(('diag', fname)))
        plt.savefig('%s_age_v.png' % fig_name, dpi=300)
        plt.close()
    return


def bigplots(agb_tracks, infile):
    if type(agb_tracks[0]) == str:
        agb_tracks = [get_numeric_data(a) for a in agb_tracks]
    out_fig = os.path.join(infile.diagnostic_dir, 'hrd_%.4f.png' % agb_tracks[0].metallicity)
    plot_title = '$\dot{M}_{\\rm M13}\ Z=%.4f$' % agb_tracks[0].metallicity
    nagb_tracks = len(agb_tracks)
    fig, (axs) = setup_multiplot(nagb_tracks,
                                 ylabel='$\log\ L\ (L_\odot)$',
                                 xlabel='$\log\ T_{\\rm eff}\ (K)$',
                                 title=plot_title,
                                 subplots_kwargs={'figsize': (30, 30),
                                                  'squeeze': True})
    axs = axs.flatten()
    [hrd_slopes(agb_tracks[i], ax=axs[i]) for i in range(nagb_tracks)]
    plt.savefig(out_fig, dpi=300)
    ylabel = ['$C/O$', '$\log\ L\ (L_\odot)$', '$\log\ T_{\\rm eff}\ (K)$']
    ycol = ['C/O', 'logl', 'logt']
    for i in range(len(ylabel)):
        fig, (axs) = setup_multiplot(nagb_tracks,
                                     ylabel=ylabel[i],
                                     xlabel='${\\rm Age (yr)}$',
                                     title=plot_title,
                                     subplots_kwargs={'figsize': (30, 30),
                                                      'squeeze': True})
        axs = axs.flatten()
        [age_vs_plot(agb_tracks[j], infile, ycol=ycol[i], ax=axs[j], annotate=True,
                     xlabels=False, ylabels=False, save_plot=False)
         for j in range(len(agb_tracks))]
        out_fig = out_fig.replace('hrd', 'age_v_%s' % ycol[i].lower().replace('c/o',
                                                                              'co'))
        plt.savefig(out_fig, dpi=300)


def hrd_slopes(track, ax):
    logl = track.data_array['L_star']
    logt = track.data_array['T_star']
    x = np.linspace(min(logt), max(logt))

    [ax.plot(np.sort(logt[r]), logl[r][np.argsort(logt[r])], color='red', lw=2)
     for r in track.rising if len(r) > 0]
    [ax.plot(x, track.fits[i][0] * x + track.fits[i][1], '--', color='blue',
             lw=0.5) for i in range(len(track.fits))]
    [ax.plot(logt[q], logl[q], 'o', color='blue') for q in track.mins]


def plot_ifmr(imfrfile, ax=None, zs=None, data_mi=None, data_mf=None,
              data_mierr=None, data_mferr=None):
    mi, mf, z = np.loadtxt(imfrfile, unpack=True)
    zinds, unz = get_unique_inds(z)
    if zs is None:
        zs = np.unique(z)
    cols = discrete_colors(len(zs))
    cols = cols * len(zinds)
    if ax is None:
        fig, ax = plt.subplots()
    [ax.plot(mi[zinds[i]], mf[zinds[i]], color=cols[i], label=str(z[unz[i]]))
        for i in range(len(unz)) if z[unz[i]] in zs]
    [ax.plot(mi[zinds[i]], mf[zinds[i]], 'o', ms=4, color=cols[i],
              mec='white', alpha=0.5) for i in range(len(unz)) if z[unz[i]] in zs]
    if data_mf is not None:
        if data_mierr is not None:
            from matplotlib.patches import Rectangle
            bottom_left = (data_mi - data_mierr/2., data_mf - data_mferr/2.)
            width = data_mierr
            height = data_mferr
            rect = Rectangle(bottom_left, width, height, color='black', alpha=.25)
            ax.add_patch(rect)
    ax.legend(loc=2, frameon=False)
    ax.set_xlabel(r'$M_i/M_{\odot}$', fontsize=20)
    ax.set_ylabel(r'$M_f/M_{\odot}$', fontsize=20)
    plt.savefig(imfrfile.replace('dat', 'png'))
    #plt.close()
    return ax


def plot_cluster_test(lifetimesfile):
    def cluster_data():
        cmass = np.array([5.9, 4.75, 3.85, 3.17, 2.66, 2.17, 1.66, 1.18, 0.82])
        ctauc = np.array([0.032,  0., 0., 0., 2.8, 2.59, 1.57, 0., 0.])
        ecp = np.array([0.075, 0.5, 0.07, 0.9, 2.21, 0.67, 0.71, 1.49, 0.66])
        ecm = np.array([0.026, 0., 0., 0., 1.34, 0.55, 0.51, 0., 0.])
        ctaum = np.array([0.26, 2.19, 0.19, 0.79, 2.8, 3.77, 1.74, 2.62, 0.66])
        emp = np.array([0.13, 1.47, 0.18, 1.81, 2.21, 0.79, 0.74, 3.44, 0.])
        emm = np.array([0.090, 0.940, 0.100, 0.660, 1.340, 0.660, 0.540, 1.690,
                    100.000])
        return cmass, ctauc, ecp, ecm, ctaum, emp, emm

    z, mass, tauc, taum = np.loadtxt(lifetimesfile, unpack=True)
    zinds, unz = get_unique_inds(z)
    cols = discrete_colors(len(zinds))

    ax1, ax2 = two_panel_plot_vert(fign=3)
    ax2.set_ylabel(r'$\tau_M\ (\rm{Myr})$', fontsize=20)
    ax1.set_ylabel(r'$\tau_C\ (\rm{Myr})$', fontsize=20)
    ax1.set_xlabel(r'$M_{TO}\ (\rm{M}_\odot)$', fontsize=20)

    cmass, ctauc, ecp, ecm, ctaum, emp, emm = cluster_data()
    ax1.errorbar(cmass, ctauc, yerr=[ecm, ecp], fmt='o', color='black',
                 label='LMC')
    ax2.errorbar(cmass, ctaum, yerr=[emm, emp], fmt='o', color='black')

    for i in range(len(unz)):
        ax1.plot(mass[zinds[i]], tauc[zinds[i]], color=cols[i],
                 label=str(z[unz[i]]))
        ax2.plot(mass[zinds[i]], taum[zinds[i]], color=cols[i])

    [ax.set_ylim(0, ax.get_ylim()[1]) for ax in [ax1, ax2]]
    ax1.legend(loc='best', ncol=2, frameon=False, numpoints=1)
    plt.savefig(lifetimesfile.replace('dat', 'png'))
    logger.info('wrote {}'.format(lifetimesfile.replace('dat', 'png')))
    plt.close()
    return


def get_unique_inds(ntp):
    un = np.unique(ntp)
    if un.size == 1:
        logger.warning('only one themal pulse.')
        return un, list(ntp).index(u)
    else:
        # this is the first step in each TP.
        iTPs = [list(ntp).index(u) for u in un]
        # The indices of each TP.
        TPs = [np.arange(iTPs[i], iTPs[i + 1]) for i in range(len(iTPs) - 1)]
        # don't forget the last one.
        TPs.append(np.arange(iTPs[i + 1], len(ntp)))
        return TPs, iTPs
