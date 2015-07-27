# Copyright (C) 2014 Ezequiel Castillo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import types
import sys
import molekule
from keys import KeyContainer, keyTypes, mandatoryKeys
from vmd import take_snapshot, plotIt, mergeImage, FitBlock, set_file
from inputgroup import GroupContainer, InputGroup
from base import patterns, BaseContainer
import matplotlib.pyplot as plt
import subprocess
#from Stretch import *

#__all__ = ['SiestaObj', 'Stretch']
#__all__ = ['SiestaObj']

class SiestaError(Exception):
    pass


class SiestaObj(object):
    """
    Process or creates and input file for SIESTA. It requires the input
    filename wheter for reading or processing.
    """

    siestaCounter = -1

    def __init__(self, siestaFdf=None, siestaOut=None, enerFile=None,
                 siestaDir=None, siestaANI=None):
        '''Main siesta Object'''

        SiestaObj.siestaCounter += 1

        if siestaFdf is None:
            self.siestaFdf = 'input.fdf'

        else:
            self.siestaFdf = siestaFdf

        if siestaDir is None:
            self.siestaDir = os.getcwd()
        else:
            self.siestaDir = siestaDir

        if siestaOut is None:
            self.siestaOut = 'output.out'
        else:
            self.siestaOut = siestaOut

        if os.path.isfile(os.path.join(self.siestaDir, self.siestaFdf)):
            self._readFdf()
            self.systemLabel = self.Keys['systemlabel'].value
            self.siestaXyz = self.systemLabel + '.xyz'
            self.siestaANI = self.systemLabel + '.ANI'
            self.siestaMDE = self.systemLabel + '.MDE'
            self._testFinished()

        self.baseDir = os.path.basename(self.siestaDir)

        # Try to read siestaFdf file



        # This is for Stretch compatibility
        #try:
            #self._step = float(os.path.basename(self.siestaDir))
        #except:
            #pass

    def checkMandatory(self):
        '''Check for mandatoryKeys.'''
        for k in mandatoryKeys:
            if isinstance(k, types.ListType):
                declared = False
                for sk in k:
                    if sk in self.Keys:
                        declared = True
                        break
                if not declared:
                    raise SiestaError('Mandatory key %s not defined.' % (sk,))
            else:
                try:
                    self.Keys[k]
                except KeyError as err:
                    print('Mandatory key %s not defined.' % (err,))

    def _readFdf(self):
        # Container of current keys found in input file
        self.Keys = KeyContainer()
        self.inputGroups = GroupContainer()

        with open(os.path.join(self.siestaDir, self.siestaFdf), 'r') as f:
            l = f.readline()
            while l:
                if patterns['inputgroup'].match(l):
                    # We are in the presence of an input group
                    igl = l  # inputgroup line
                elif patterns['blankline'].match(l):
                    # A blank line, but create empty inputGroup
                    igl = None

                # Now we check if variable name 'ig' is defined. If not, set it
                # to empty inputGroup
                try:
                    _ = igl
                except NameError:
                    #ig = InputGroup()
                    igl = None

                if igl is None:
                    igl = '#--Unnamed group\n'

                self.inputGroups.update_group(igl)

                if not patterns['comment'].match(l) or not patterns['endc'].match(l):
                    for t in keyTypes:
                        m = re.match(t._pattern, l)
                        if m:
                            kt = t(m, f=f, path=self.siestaDir)  # keyType is an instance of BaseKey
                            self.Keys.addKey(kt)
                            self.inputGroups.add_key_to_group(keyword=kt, group=igl)
                            break

                l = f.readline()

        # Check chemicalspecieslabel in atomiccoordinatesandatomicspecies
        # First we get the species

        #self.species = dict([l[0:2] for l in self.Keys.chemicalspecieslabel.value])
        self.species = dict([l.split()[0:2] for l in self.Keys.chemicalspecieslabel.value])
        for sp in self.species.keys():
            self.species[sp] = molekule.atno_to_symbol[int(self.species[sp])]

        # Then coordinate lines
        for k in ['atomiccoordinatesandatomicspecies', 'zmatrix']:
            if k in self.Keys:
                self.coords = self.Keys[k].coords
                # 'atomiccoordinatesandatomicspecies' has species labeled at
                # colum 4, whereas 'zmatrix' has it at column 1
                if k == 'atomiccoordinatesandatomicspecies':
                    lc = 3      # LabeledColumn
                elif k == 'zmatrix':
                    lc = 0
                break

        try:
            #for s in map(list, zip(*self.coords))[lc]:
                #if not s in self.species:
                    #raise SiestaError('Specie %s not defined in ChemicalSpeciesLabel block' % (s,))

            # Variation!!
            atoms = []
            for c in self.coords:
                s = c.split()
                if s[lc] not in self.species:
                    raise SiestaError('Specie %s not defined in ChemicalSpeciesLabel block' % (s,))
                #atoms.append(molekule.Atom(symbol=self.species[s[0]], pos=s[1:4]))
                atoms.append(molekule.Atom(symbol=self.species[s[lc]], pos=s[0:3]))

            #for c in self.coords:
                #atoms.append(molekule.Atom(symbol=self.species[c[0]], pos=c[1:4]))
            self.system = molekule.Molecule(atoms=atoms)
        except AttributeError:
            pass

    def _loadFromMol(self, mol):
        self.system = mol
        self.species = {i+1: s for i, s in enumerate(mol.get_species())}

    def _genFdf(self, fname=None, action='w'):
        """_genFdf(self, fname=None)

        Generate an input file for siesta.

        Parameters
        ----------
        fname : string
                Specifies full path output filename.

        action : string
                 Should be either 'w' (creates a new file, default) or 'a'
                 (appends).

        Returns
        -------
        Nothing
        """

        # Uncomment the following in order to control that everything is cool.
        #self.checkMandatory()

        if fname is None:
            fname = self.siestaFdf

        with open(os.path.join(self.siestaDir, fname), action) as f:
            f.write(self.inputGroups.get_string_from_all_groups())

    def _get_frameNr(self):
        with open(os.path.join(self.siestaDir, self.siestaANI), 'r') as f:
            fn = 0
            l = f.readline()
            while l:
                atno = int(l)
                list_mol = [l]
                for _ in xrange(atno + 1):   # + 1 because of the second blank line
                    f.readline()
                fn += 1
                l = f.readline()
        return fn

    def _get_energies(self, e=None, zref='min'):
        """_get_energies(e=None, zref=None)

        Get some type of energy from output file.

        Parameters
        ----------
        e : 'eks' or 'total'
            Specifies if returned value shall be Kohn-Sham energies ('eks') or
            the final energy of the current siesta run ('total'). If not
            supplied, return both Kohn-Sham an Total energies as tupple like
            ([eks], etotal).
        zref : 'min' or 'max'
            Specifies where to reference the zero of energy. 'min' sets minimum
            energy to zero and 'max' sets maximum energy to zero.

        Returns
        -------
        Kohn-Sham energies as list and/or total energy as float, depending on
        the e parameter.
        """

        if e is not 'total' and e is not 'eks':
            raise IOError("'e' must be either 'ks' or 'total' or None")

        with open(os.path.join(self.siestaDir, self.siestaOut), 'r') as f:
            eks = []
            for l in f:
                if e is 'ks' or e is None:
                    m_eks = patterns['eks'].match(l)
                    if m_eks:
                        eks.append(m_eks.group(1))
                if e is 'total' or e is None:
                    m_etotal = patterns['etotal'].match(l)
                    if m_etotal:
                        etotal = m_etotal.group(1)
        if e is 'ks':
            return eks
        elif e is 'total':
            try:
                _ = etotal
                return float(etotal)
            except UnboundLocalError:
                print 'Warning: not finished siesta Run at %s' % self.siestaDir
                return 0
        elif e is None:
            return eks, etotal

    def set_StepMinimizationFrames(self):
        ''' Read "systemlabel.ANI" and "systemlabel.MDE" file (so
        "writemdhistory" and "writemdxmol" keys must be set to "True") in order
        to extract the coordinates and energies of each minimization step. '''

        xyzNoLines = len(self.system) + 2

        aniFrames = []
        mdeStepEnergy = []
        if self.is_initialSameAsFinal():
            with open(os.path.join(self.siestaDir, self.siestaXyz), 'r') as f:
                aniFrames.append(list(f.readlines()))

            mdeStepEnergy.append([0, self._get_energies(e='total')])

        else:
            with open(os.path.join(self.siestaDir, self.siestaANI), 'r') as f:
                l = f.readline()
                while l:
                    aFrame = []
                    for _ in xrange(xyzNoLines):
                        aFrame.append(l)
                        l = f.readline()
                    aniFrames.append(aFrame)

            with open(os.path.join(self.siestaDir, self.siestaMDE), 'r') as f:
                f.readline()
                for l in f.readlines():
                    sl = l.split()
                    mdeStepEnergy.append([int(sl[0]), float(sl[2])])

        a, b = len(aniFrames), len(mdeStepEnergy)
        if a != b:
            raise SiestaError('Missmatch: got %i frames from ANI file and %i steps from MDE file' % (a, b))

        self.StepMinimizationFrames = []
        for i in xrange(a):
            step, energy = mdeStepEnergy[i]
            frame = SiestaFrame(name='step'+str(step))
            frame.set_energy(energy)
            frame.set_step(step)
            frame.load_fromList(aniFrames[i])
            self.StepMinimizationFrames.append(frame)

    def is_initialSameAsFinal(self):
        if self._FINISHED:
            if not os.path.isfile(os.path.join(self.siestaDir, self.siestaANI)):
                return True
    def set_FinalMinimizationFrame(self):
        #if self._FINISHED:
            #try:
                #self.FinalMinimizationFrame = self.StepMinimizationFrames[-1]
            #except AttributeError:
                #try:
                    #self.set_StepMinimizationFrames()
                #except ValueError:
                    #xyzCoords = []
                    #with open(os.path.join(self.siestaDir, self.siestaXyz), 'r') as f:
                        #xyzCoords.append(list(f.readlines()))

                    #self.FinalMinimizationFrame = SiestaFrame()


                #self.FinalMinimizationFrame = self.StepMinimizationFrames[-1]
                #try:
                    #self.FinalMinimizationFrame.set_step(float(self.baseDir))
                #except ValueError:
                    #self.FinalMinimizationFrame.name = self.baseDir
        if self._FINISHED:
            with open(os.path.join(self.siestaDir, self.siestaXyz), 'r') as f:
                coords = f.readlines()
            ener = self._get_energies(e='total')
            self.FinalMinimizationFrame = SiestaFrame()
            self.FinalMinimizationFrame.load_fromList(coords)
            self.FinalMinimizationFrame.set_energy(ener)
            try:
                self.FinalMinimizationFrame.set_step(float(self.baseDir))
            except ValueError:
                self.FinalMinimizationFrame.name = self.baseDir



        else:
            raise SiestaError('Cannot set final frame beacuse the siesta run is not finished.')

    def get_imagesFromStepMinimizationFrames(self, VMDcmdFile=None):
        for frame in self.StepMinimizationFrames:
            frame.get_image(cwd=self.siestaDir, cmdFile=VMDcmdFile,
                            pngOut='frame%04i.png'%(frame.step))

    def get_imagesFromFinalMinimizationFrame(self, VMDcmdFile=None):
        self.FinalMinimizationFrame.get_image(cwd=self.siestaDir,
                                              cmdFile=VMDcmdFile,
                                              pngOut='final%04i.png'%(SiestaObj.siestaCounter))

    #def gen_movie(self):
        #for frame in self.StepMinimizationFrames

    def plot_MinimizationEnergies(self):
        self.set_StepMinimizationFrames()
        x = map(lambda fr: fr.step, self.StepMinimizationFrames)
        y = map(lambda fr: fr.energy, self.StepMinimizationFrames)
        ymin = min(y)
        y = [e - ymin for e in y]
        #y = y - y.min()
        fig = plt.figure()
        ax = fig.add_subplot(111, axisbg='lightgray')
        ax.grid(axis='y')
        ax.set_xlabel(r'Minimization Step')
        ax.set_ylabel(r'Energy [eV]')
        ax.set_xmargin(0.1)
        ax.set_ymargin(0.05)
        #ax.plot(x, y, '-o', ms=20, lw=2, alpha=0.7, mfc='orange')
        ax.plot(x, y, '-o')
        plt.show()

    def _testFinished(self):
        """_testFinished()

        Test if current Siesta run is finished or not.

        Returns
        -------
        True or False """

        try:
            with open(os.path.join(self.siestaDir, self.siestaOut), 'r') as f:
                for l in f:
                    m = patterns['finished'].match(l)
                    if m:
                        self._FINISHED = True
                        return True
                self._FINISHED = False
                return False
        except IOError:
            self._FINISHED = False

    def _plotIt(self, x, y):
        """_plotIt(x=None, y=None)

        Generate a plot given 'x' and 'y' and sets the 'plot' attribute, which
        retains the file name of the generated plot image.

        Parameters
        ----------
        x : list of floats
        y : list of floats

        Returns
        -------
        Nothing."""

        self.plot = plotIt(x, y, cwd=self.siestaDir,
                pngOut=os.path.join(self.siestaDir, 'siestaPlot.png'))

    def _mergeImage(self):
        self.mergedImage = mergeImage(self.finalFrameIma, self.plot)

    def run(self, simulate=False):
        ifile = open(os.path.join(self.siestaDir, self.siestaFdf), 'r')
        ofile = open(os.path.join(self.siestaDir, self.siestaOut), 'w')
        if not simulate:
            proc = subprocess.Popen('siesta', stdin=ifile, stdout=ofile,
                                    shell=True, cwd=self.siestaDir)
            proc.communicate()
        ofile.flush()
        ofile.close()
        ifile.close()


class SiestaFrame(molekule.Molecule):
    """ This class intends to be an instance of a siesta step, whether if it
    correponds to a final minimization run (name='Final') or an intermidiate
    minimization step (name='Partial'). """

    def set_step(self, s):
        self.step = s

    def set_energy(self, e):
        self.energy = e


if __name__ == '__main__':
    pass
    #cgDir = os.path.join(os.path.dirname(__file__), os.path.pardir, 'samples', 'siesta', 'cg')
    #A = SiestaObj(siestaDir=cgDir)
