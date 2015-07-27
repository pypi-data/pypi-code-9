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
#import molekule
from main import SiestaObj
from molekule import render, Molecule, Cell
from matplotlib import pyplot as plt
from vmd import DiffData
from numpy import array, linspace, polynomial, where, polynomial, linalg
import re
import shutil
from scipy.optimize import curve_fit
#from .main import SiestaObj

from pint import UnitRegistry
ureg = UnitRegistry()

def floatable(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def replace_TextInFile(pattern, string, fn):
    #fout = open(fn+'.temp'  , 'w')
    s = ''
    with open(fn, 'r') as f:
        for l in f:
            if re.search(pattern, l):
                s += re.sub(pattern, string, l)
                #fout.write(re.sub(pattern, t, l))
            else:
                #fout.write(l+'\n')
                s += l
    #shutil.move(fn+'.temp', fn)
    return s



class Test(object):

    def __init__(self, testName=None, testPath=None, testSteps=None,
                 testFiles=None, testModFiles=None, replacePattern=None,
                 testFilesDir= None, loadTest=False):

        if testName is None:
            raise IOError('"testName" must be supplied!')

        self.testName = testName

        if testPath is None:
            self.testPath = os.getcwd()
        else:
            self.testPath = testPath

        try:
            if testSteps:
                self.testSteps = testSteps
        except ValueError:
            if testSteps.any():
                self.testSteps = testSteps

        self.testFiles = testFiles
        self.testModFiles = testModFiles

        if testFilesDir:
            self.testFilesDir = testFilesDir
        else:
            self.testFilesDir = self.testPath

        if replacePattern:
            self.replacePattern = replacePattern
        else:
            self.replacePattern = r'\$' + r'%s' % (self.testName, )

        if loadTest:
            self.load_TestFromPath()
            self.set_TestSteps()
            self.set_TotalFinalEnergies(ref='m')

    def load_TestFromPath(self):
        """ Load test from path. Currently only numerical test are supported,
        i.e.  the key which is being tested has a numerical value (e.g.
        Stretch, Box, EnergyShift, etc.)"""

        # dD: dummyDir
        dD = [os.path.join(self.testPath, d) for d in os.listdir(self.testPath)]
        dD = filter(os.path.isdir, dD)
        dD = map(os.path.basename, dD)
        dD = filter(floatable, dD)
        dD = [os.path.join(self.testPath, d) for d in dD]

        dD = sorted([SiestaObj(siestaDir=d) for d in dD],
                                      key=lambda sObj: float(sObj.baseDir))

        self.TestStepObjects = filter(lambda sObj: sObj._testFinished(), dD)

    def create_Test(self, displace_atoms=None, run=False):
        os.chdir(self.testPath)
        if os.path.isdir(self.testName):
            while True:
                s = raw_input('--> Directory "%s" already exists. Continue with or Delete it?([c]/d)' % self.testName)
                if s in ["d", "D", "n"]:
                    shutil.rmtree(self.testName)
                    os.mkdir(self.testName)
                    break
                elif s in ["c", "C", "y"]:
                    break
                else:
                    print "Not valid answer."
        else:
            os.mkdir(self.testName)

            #raise IOError('Directory "%s" already exists. Delete it to create new one.' % self.testName)
        os.chdir(self.testName)
        for i, t in enumerate(self.testSteps):
            os.mkdir(str(t))
            os.chdir(str(t))
            for f in self.testFiles:
                fullPath = os.path.join(self.testFilesDir, f)
                if f in self.testModFiles:
                    with open(f, 'w') as fn:
                        fn.write(replace_TextInFile(self.replacePattern,
                                                    str(t), fullPath))
                else:
                    shutil.copy(fullPath, '.')
            if run:
                pass


            os.chdir(os.pardir)

    def set_TestSteps(self):
        #self.TestSteps = map(lambda sObj: sObj.baseDir, self.TestStepObjects)
        self.TestSteps = array([float(sObj.baseDir) for sObj in self.TestStepObjects]) * ureg.angstrom

    def set_StepMinimizationEnergies(self, ref=None):
        self.StepMinimizationEnergies = []
        for sObj in self.TestStepObjects:
            sObj.set_StepMinimizationFrames()
            for frame in sObj.StepMinimizationEnergies:
                self.StepMinimizationEnergies.append(frame.energy)

        if ref:
            self.StepMinimizationEnergies = self._get_referenced(ref, self.StepMinimizationEnergies)

    def set_TotalFinalEnergies(self, ref=None):
        """
        'ref' is either m (minimum), 'M' (maximum) or None for referencing
        energies
        """
        self.TotalFinalEnergies = []
        for i, sObj in enumerate(self.TestStepObjects):
            sObj.set_FinalMinimizationFrame()
            sObj.FinalMinimizationFrame.idx = i
            self.TotalFinalEnergies.append(sObj.FinalMinimizationFrame.energy)

        if ref:
            self.TotalFinalEnergies = self._get_referenced(ref, self.TotalFinalEnergies)

        self.TotalFinalEnergies = array(self.TotalFinalEnergies) * ureg.eV

    def _get_referenced(self, ref, list_):
        if ref == 'm':
            r = min(list_)
        elif ref == 'M':
            r = max(list_)
        else:
            raise IOError('ref must be either "m" (minimum), "M" (maximum) or "None".')

        return [e - r for e in list_]

    def plot_energy(self, title=None, final=False, step=False,
                    poli='Chevbyshev', pngOut=None, left=None, right=None,
                    **kwargs):
        self.set_TotalFinalEnergies(ref='m')
        self.set_TestSteps()
        if final is True and step is True:
            raise IOError('Only "final" or "step" can be True at the same time')
        elif final is False and step is False:
            final = True

        if step is True:
            y_data = self.StepMinimizationEnergies
        elif final is True:
            y_data = self.TotalFinalEnergies

        x_data = self.TestSteps

        render.FitBlock(x=x_data, y=y_data, sysName=title, poli=poli,
                        pngOut=pngOut, left=left, right=right)

        pass

    def plot_Test(self, force=True, grad=8, fitm=0, fitM=-1):
        if not self.TestSteps.any():
            self.set_TestSteps()
        elif not self.TotalFinalEnergies.any():
            self.set_TotalFinalEnergies(ref='m')
        x = array(self.TestSteps)
        y = array(self.TotalFinalEnergies)
        ebind = max(y) - min(y)

        #fig = plt.figure(figsize=(8,6), dpi=100)
        #fig = plt.figure()
        #fig.figsize = 8, 6
        #fig.dpi = 100
        #ax = fig.add_subplot(111)
        #ax.set_xlabel('Stretch Distance (nm)')
        #ax.set_ylabel('Energy (eV)')
        #ax.scatter(x, y, s=50, c='yellow', alpha=0.5)
        ffit = polynomial.chebyshev.Chebyshev.fit(x[fitm:fitM], y[fitm:fitM],
                                                  grad)

        if force is True:
            ffitd = polynomial.chebyshev.Chebyshev.deriv(ffit)
            dx, dy = ffitd.linspace()
            dy *= 1.60217733
            #xfit = linspace(x[0], x[-1], num=len(x)*20)
            #ffit = polynomial.Chebyshev.fit(dx, dy, grad)

            f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
            f.suptitle(self.testName, fontsize=14, fontweight='bold')
            #fig = plt.figure(figsize=(8,6), dpi=100)
            #fig = plt.figure()
            #fig.figsize = 8, 6
            #fig.dpi = 100
            ax1.set_ylabel('Energy [eV]')
            ax1.grid()
            ax2.grid()
            ax2.set_ylabel('Force [nN]')
            ax2.set_xlabel('Stretching distance [\AA]')
            ax2.axhline(linestyle='--', color='gray', linewidth='2')
            f.subplots_adjust(hspace=0)
            #f.suptitle(sysName)
            ax1.scatter(x, y, s=30, facecolors='none', edgecolors='blue')
            ax2.plot(dx, dy, '-g')
            #ax = fig.add_subplot(111)
            #ax.set_xlabel('Stretch Distance (nm)')
            #ax.set_ylabel('Force (nN)')
            #ax.scatter(dx, dy, s=50, c='red', alpha=0.5)
            #ax.plot(xfit, ffit(xfit), lw=2, c='orange')
            ax1.text(0.9, 0.2, r'E$_{\textrm{bind}}$ = %.2f eV' % (ebind,),
                            verticalalignment='top', horizontalalignment='right',
                            transform=ax1.transAxes,
                            color='blue', fontsize=15)
            ax2.text(0.9, 0.9, r'F$_{\textrm{max}}$ = %.2f nN' % (max(dy),),
                            verticalalignment='top', horizontalalignment='right',
                            transform=ax2.transAxes,
                            color='green', fontsize=15)
        else:
            f = plt.figure()
            f.suptitle(self.testName, fontsize=14, fontweight='bold')
            ax = f.add_subplot(111)
            ax.grid()
            ax.scatter(x, y, s=50, facecolors=None, edgecolors='blue')
            plt.show()


        plt.show()

    def gen_xyzMovie(self, filename='xyzMovie.xyz', full=True):
        for step in self.TestStepObjects:
            step.set_StepMinimizationFrames()
        with open(filename, 'w') as f:
            for step in self.TestStepObjects:
                for fr in step.StepMinimizationFrames:
                    f.write(fr.write_totring())

    def fullMovie(self):
        pass

    def bm_fit(self, stype='fcc'):

        def bm_eos(a, e0, a0, b0, db0, f):
            # This fix pint unit error
            #a = a * ureg.angstrom
            #a0 = a0 * ureg.angstrom
            #e0 = e0 * ureg.eV
            #b0 = b0 * ureg.eV / ureg.angstrom**3
            aa = (a0/a)**2
            bb = aa - 1
            return e0 + 9.*a0**3*b0/(16.*f) * (bb**3*db0 + bb**2 * (6.-4.*aa))

        #def bm_eos(v, e0, v0, b0, db0):
            #vv = (v0/v)**(2./3)
            #bb = vv - 1
            #return e0 + 9.*v0*b0/16. * (bb**3*db0 + bb**2 * (6.-4.*vv))

        if stype is 'fcc':
            factor = 4
        elif stype is 'bcc':
            factor = 2
        else:
            raise IOError('"stype" must be either fcc or bcc.')

        self.set_TotalFinalEnergies(ref='m')

        x = self.TestSteps.magnitude
        #x = x**3
        y = self.TotalFinalEnergies.magnitude

        #popt, pcov = curve_fit(bm_eos, x, y, p0=[y.min(), x[where(y==y.min())[0][0]], 1, 1], maxfev=1000000)
        #HERE
        popt, pcov = curve_fit(lambda a, e0, a0, b0, db0: bm_eos(a, e0, a0, b0,
                                                                 db0, factor),
                               x, y, p0=[y.min(), x[where(y==y.min())[0][0]],
                                         1, 1], maxfev=1000000)

        self.popt_bm = popt
        e0, a0, b0, db0 = popt
        self.a0 = a0 * ureg.angstrom
        self.b0 = b0 * ureg.eV / (ureg.angstrom ** 3)
        self.b0 = self.b0.to(ureg.gigapascal)
        #e0, v0, b0, db0 = popt


        xf = linspace(x[0], x[-1], 100)
        yf = bm_eos(xf, e0, a0, b0, db0, factor)
        #yf = bm_eos(xf, e0, v0, b0, db0)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.testName)
        ax.set_xlabel(r'Lattice Parameter [\AA]')
        ax.set_ylabel('Energy [eV]')
        ax.scatter(x, y, c='red', s=50, alpha=0.8)
        ax.plot(xf, yf, 'b-', lw=2)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        #ax.text(0.9, 0.9, r'\noindent $a_0=%.2f$ \AA \\ $B_0=%.3f$ GPa' % (v0, b0*1.6021*10**2),
        #ax.text(0.9, 0.9, r'\noindent $a_0=%.2f$ \AA \\ $B_0=%.3f$ GPa' %
        ax.text(0.9, 0.9, r'\begin{align*} a_0&=%.2f \: \mbox{\AA} \\ B_0&=%.3f \: \mbox{GPa} \end{align*}' %
                (self.a0.magnitude, self.b0.magnitude), size='large',
                verticalalignment='top', horizontalalignment='right',
                transform=ax.transAxes, backgroundcolor='white')

        plt.show()

    def run_stretching(self, moveAtoms=[0, 10], d=[0,0,0.1], totalSteps=40,
                       xyzFile='siesta.xyz', startCellFile='vectors.data',
                       needed_files=None, restart=False, simulate=False,
                       lastStep=None):

        #moveAtoms = (14,27)
        #d = array([0,0,0.1])
        #totalSteps = 80

        #copy_files = ['Ag.psf', 'C.psf', 'H.psf', 'N.psf', 'input.fdf']
        #copy_needed_files = ['siesta.DM', 'siesta.XV']

        fia, lia = moveAtoms    # First and last index of moving atom

        if lastStep:
            if lastStep is 'auto':
                start = max([float(f) for f in os.listdir(self.testPath) if
                             os.path.isdir(f)])
            else:
                start = float(lastStep)
        else:
            start = 0.0

        for i in xrange(totalSteps):
            disp = '%.1f' % (start + i * linalg.norm(d),)
            if not os.path.isdir(disp):
                os.mkdir(disp)
            if i is 0:
                if os.path.isfile(disp):
                    S = SiestaObj(siestaDir=disp)
                    if not S._FINISHED:
                        S.run(simulate)
                    continue
                else:
                    M = Molecule(fromFile=xyzFile)
                    C = Cell(fromFile=startCellFile)
                    for f in needed_files:
                        shutil.copy(f, disp)
            else:
                prev_disp = '%.1f' % (start + (i-1) * linalg.norm(d),)
                for f in needed_files:
                    shutil.copy(os.path.join(prev_disp, f), disp)
                M = Molecule(fromFile=os.path.join(prev_disp, xyzFile))
                M[fia:lia+1] + d
                C = Cell(fromFile=os.path.join(prev_disp, 'vectors.data'))
                C.a3 = C.a3 + d

            for f in self.testFiles:
                shutil.copy(f, disp)
            M.write_siestaCoords(os.path.join(disp, 'coordinates.data'))
            M.write_siestaSpecies(os.path.join(disp, 'species.data'))
            C.write_cellVectors(os.path.join(disp, 'vectors.data'))
            S = SiestaObj(siestaDir=disp)
            S.run(simulate=simulate)
            del(M)
            del(C)
            del(S)


if __name__ == '__main__':
    stretchDir = os.path.join(os.path.dirname(__file__), os.path.pardir,
                              'samples', 'siesta', 'stretch')
    A = Test(testName='NH2.spin', testPath=stretchDir, loadTest=True)
