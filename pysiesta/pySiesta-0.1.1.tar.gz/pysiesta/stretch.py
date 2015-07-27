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
import numpy as np
from pysiesta.vmd import *
from pysiesta.main import SiestaObj

__all__ = ['StretchSiesta']

class StretchSiesta(object):
    """
    Gather all stretching info (energy, force (hopefully), and figures
    (obtained from vmd))

    Options:
        infile:
        outfile:
        path:
        energy:
    """

    def __init__(self, path=None):

        if path is None:
            self.path = os.getcwd()
        else:
            self.path = path

        self.frames = []

        #os.chdir(self.path)

        #testD = filter(os.path.isdir, os.listdir(self.path))
        #testD = filter(float, testD])
        testD = filter(float, map(os.path.basename, filter(os.path.isdir, [os.path.join(self.path, d) for d in os.listdir(self.path)])))
        testD = [os.path.join(self.path, d) for d in testD]
        self.stretchSteps = [SiestaObj(siestaDir=d) for d in testD]
        for sObj in self.stretchSteps:
            sObj._step = float(os.path.basename(sObj.siestaDir))

        self.eks = []
        self.etotal = self.get_totalEner()
        self._get_steps()
        self.get_finalFrames()
        self._fn = 0                      # Frames number

        # Now we test how many xyz frames we have in the ANI file and compare
        # them with eks.
        if not self._fn == len(self.eks):
            print 'Warning: frames and minimzation steps do not match'
            #with open(self.infile, 'r') as inf:
                #line = inf.readline()

                #while line:
                    #atno = int(line)
                    #list_mol = [line]
                    #for _ in xrange(atno+1):
                        #list_mol.append(inf.readline())
                    #self.frames.append(Frame(list_mol, as_list=True))
                    #line = inf.readline()

            #with open(self.siestaOut, 'r') as f:
                #for line in f:
                    #match = eks_c.match(line)
                    #if match:
                        #self.ener_l.append(match.group(1))

            #os.chdir(os.pardir)

        #for i, frame in enumerate(self.frames):
            #frame.energy = self.ener_l[i]
            #frame.steps = range(i + 1)
            #frame.prev_ener = self.ener_l[:i + 1]

            #frame.plot_energy(range(i+1), self.ener_l[:i+1])

    #def movie(self):

        # First we get the parameters of the final frame.
        #maxSteps = self.frames[-1].steps

        #pass

    #def get_frameNr(self, d):
        #with open(os.path.join(d, self.siestaANI), 'r') as f:
            #fn = 0
            #l = f.readline()
            #while l:
                #atno = int(l)
                #list_mol = [l]
                #for _ in xrange(atno + 1):   # + 1 because of the second blank line
                    #f.readline()
                #fn += 1
                #l = f.readline()

        #return fn

    def get_totalEner(self, ref='min'):
        '''get_totalEner()

        Return a list containing total energy for each stretching distance.
        They can be referenced by its minimum or maximum energy.

        Parameters
        ----------
        ref : 'min' or 'max'

        Returns
        -------
        A list of energies.
        '''

        if not ref is 'min' or ref is 'max':
            raise IOError("ref must be 'min' or 'max'. ('min' by default)")
        ener = map(float, [sObj._get_energies(e='total') for sObj in self.stretchSteps if sObj._testFinished()])
        #ener = np.array([(sObj._step, sObj._get_energies(e='total')) for sObj in
                #self.stretchSteps if sObj._FINISHED], dtype=float)
        if ref is 'max':
            ref = max(ener)
        elif ref is 'min':
            ref = min(ener)
        elif ref is None:
            ref = 0
        else:
            raise IOError("ref must be 'min' or 'max' or None. ('min' by default)")

        return [e - ref for e in ener]

    def get_finalFrames(self):
        for i, sObj in enumerate(self.stretchSteps):
            #sObj._plotIt()<++>
            pass

    def _get_steps(self):
        '''_get_steps()

        Get steps of current Stretch Object by setting the 'steps' attribute.
        If the siesta run is not finished it will not add the step.

        Returns
        -------
        Nothing.
        '''

        self.steps = [sObj._step for sObj in self.stretchSteps if sObj._testFinished()]

    def gen_movie(self):
        '''gen_movie()

        Populate each siesta run directory with an image that holds the points
        considered up to that stretching time. Take a snapshots of the relaxed
        structure at each stretching distance. Finally create 'movie' directory
        where the merged images of structure and energy plot are placed for
        creating a movie. All these by making use of the _plotIt method of
        SiestaObj class.

        Returns
        -------
        Create an image file at the corresponding directory level.
        '''

        for i, sObj in enumerate(self.stretchSteps):
            sObj._plotIt(self.steps[:i+1], self.etotal[:i+1])
            sObj._take_snapshot()
            sObj._mergeImage()

        movieDir = os.path.join(self.path, 'movie')
        os.mkdir(movieDir)
        for i, p in enumerate([sObj.mergedImage for sObj in self.stretchSteps]):
            imageName = 'image_' + str(i) + '.png'
            os.symlink(p, os.path.join(movieDir, imageName)) # HERE

    def gen_finalPlot(self, pngOut=None, blockFit=False):
        '''gen_finalPlot(pngOut=None, blockFit=False)

        Generate at the siestaDir level a plot of the whole stretching process. Optionally you fit all data by block.

        Parameters
        ----------
        pngOut : String
            Name of the generated image file.
        blockFit : Boolean
            Whether if it fit data or not.

        Returns
        -------
        Create an image file at the corresponding directory level.
        '''

        FitBlock(x=self.steps, y=self.etotal, poli='Chevbyshev',
                 pngOut=os.path.join(self.path, pngOut))




# TODO
#def gen_movie(self):

    #pngFiles = ' '.join


#class StretchTestCase(unittest.TestCase):
    #def testInstatiation(self):
        #self.assertTrue(Stretch(path='/home/ezequiel/Datos/Wandlowski/Sistemas/stretch'), msg='Everythin was OK')

if __name__ == '__main__':
    #unittest.main()

    # For notebook
    #A = Stretch(path='/home/ezequiel/Datos/Wandlowski/Sistemas/stretch')
    #A = Stretch(path='/home/ezequiel/Datos/Wandlowski/Sistemas/cn')
    A = Stretch(path='/home/ezequiel/Datos/ch3h2o')
    # For fcq
    #A = Stretch(path='/home/ezequiel/data/Wandlowski/Tolano/Estiramientos/bt1.slice')
