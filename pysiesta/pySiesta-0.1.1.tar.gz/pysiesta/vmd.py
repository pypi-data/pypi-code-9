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

from matplotlib import pyplot as plt
import numpy as np
import os
import re
import subprocess

vmd_commands = \
    """rotate x by -90
    mol modstyle 0 0 VDW 1.000000 12.000000
    mol material AOEdgy
    material change diffuse AOEdgy 0.680000
    material change specular AOEdgy 0.050000
    material change shininess AOEdgy 0.000000
    display depthcue off
    display shadows on
    display ambientocclusion on
    display aoambient 0.710000
    display aodirect 0.600000
    color Display Background white
    axes location Off
    render TachyonInternal vmdscene.tga
    catch { exec convert vmdscene.tga %s; rm vmdscene.tga }
    """



def take_snapshot(cwd=None, xyzFile=None, cmdFile=None, pngOut=None):
    """take_snapshot(cwd=None, xyzFile=None, cmdFile=None, pngOut=None)

    Use vmd to create a snapshot from 'xyzFile' making use of vmd commands
    stored at 'cmdFile'.

    Parameters
    ----------
    cwd : string
        Specifies where the xyzFile location is as well as the location for
        generted image files.
    xyzFile : string
        Complete file name of the coordinate file.
    cmdFile : string
        File name containing the vmd commands. If not supplied, default vmd
        commands are used.
    pngOut : string
        Image output file name.

    Returns
    -------
    Full path of the pngOut file."""

    if cwd is None:
        cwd = os.getcwd()
    if xyzFile is None:
        xyzFile = 'salida.xyz'
    if pngOut is None:
        pngOut = 'vmdscene.png'
    fXyzPath = os.path.join(cwd, xyzFile)
    os.path.isfile(fXyzPath)
    if cmdFile is None:
        cmdFile = 'vmd_commands'
    fCmdPath = os.path.join(cwd, cmdFile)
    gen_vmdCmds(cmdFile=fCmdPath, pngOut=pngOut)

    fCmdPath = os.path.join(cwd, cmdFile)
    vmd = ['vmd -f %s -size 800 800 -dispdev text -eofexit' % xyzFile]
    #vmd_exe = [vmd]
    f = open(fCmdPath, 'r')
    p = subprocess.Popen(vmd, stdin=f, shell=True, cwd=cwd)

    p.wait()
    f.close()
    #os.remove(fout)

    return os.path.join(cwd, pngOut)


def gen_vmdCmds(cmdFile='vmd_commands', pngOut='vmdscene.png'):
    if not os.path.isfile(cmdFile):
        with open(cmdFile, 'w') as f:
            vmd_cmds = vmd_commands % pngOut
            for line in vmd_cmds.split('\n'):
                f.write(line + '\n')


def plotIt(x=None, y=None, cwd=None, pngOut=None):
    """plotIt(x=None, y=None, cwd=None, pngOut=None)

    Generate a plot given 'x' and 'y'.

    Parameters
    ----------
    x : list of floats
    y : list of floats
    cwd : string
        Specifies where the location of the generted image file is.
    pngOut : string
        Image output file name.

    Returns
    -------
    Full path of the pngOut file.
    """

    fig = plt.figure(figsize=(8,6), dpi=100)
    #fig.figsize = 8, 6
    #fig.dpi = 100
    ax = fig.add_subplot(111)
    ax.set_xlabel('Stretch Distance (nm)')
    ax.set_ylabel('Energy (eV)')
    ax.scatter(x, y, s=50, facecolors=None, edgecolors='blue')
    #ax.scatter(x, y, s=50, facecolors='none', edgecolors='blue')
    ax.scatter(x[-1], y[-1], s=50, facecolors='none', edgecolors='red')
    plt.savefig(pngOut, format='png')
    plt.close()
    return os.path.join(cwd, pngOut)

def mergeImage(f1, f2, outFile='mergeim.png', cwd=None):
    """mergeImage(f1, f2)

    Merge two images making use of 'montage' Imagemagick tool. Create a file
    named as the 'outFile' argument.
    """

    if cwd is None:
        cwd = os.getcwd()
    cmd = ['montage %s %s -geometry 600x450 %s' % (f1, f2, outFile)]

    p = subprocess.Popen(cmd, shell=True, cwd=cwd)

    return os.path.join(cwd, outFile)

def createVideo(files=None, dirFile=None, outName=None):
    """createVideo(files=None, dirFile=None)

    Create a video out of a bunch of png files

    Parameters
    ----------
    files : list
        A list containing an ordered complete path and name of all files used
        for creating the movie.
    dirFile : string
        Full path of a folder containg all image files.

    Returns
    -------
    Nothing.
    """

    pngFiles = []
    if files and dirFile:
        raise IOError("Declare one of 'files' or 'dirFile' only.")

    #avconv
def DiffData(x, y):
    """DiffData(x, y)

    Derivate a set of data using the middle point derivate.

    Parameters
    ----------
    x : float list, or np.array
        x values
    y : float list, or np.array
        y values

    Returns
    -------
    'x' and 'y' values of data input derivative.
    """

    dif_x = x[1:] - x[:-1]
    x_diff = x[:-1] + dif_x/2
    dif_y = y[1:] - y[:-1]
    y_diff = dif_y/dif_x
    return x_diff, y_diff

def FitData(x, y, type='Polynomial', force=False, grad=None):
    """
    Return x and y values of best fit for x y data set by square fit of desired
    type.

    type: at this moment 'Polynomial' or 'Chebyshev' are the posible options
    """

    x_new = np.linspace(x[0], x[-1], num=len(x)*20)

    if not grad:
        grad = int(len(x)/2)+1
        if grad > 6:
            grad = 6

    if type == 'Polynomial':
        coefs = np.polynomial.polynomial.polyfit(x, y, grad)
        ffit = np.poly1d(coefs[::-1])
        ffitd = np.polyder(ffit)

    elif type == 'Chevbyshev':
        ffit = np.polynomial.Chebyshev.fit(x, y, grad)
        ffitd = np.polynomial.Chebyshev.deriv(ffit)

    if force:
        return x_new, ffit(x_new), ffitd(x_new)
    else:
        return x_new, ffit(x_new)

def FitBlock(data=None, x=None, y=None, sysName=None, poli='Polynomial',
             pngOut=None):
    """
    Linear regression of square fit of some x,y data.
    type, can be 'Polynomial' or 'Chevbyshev'.
    interv, boolean. Weather it creates a total or partial fit.
    """

    def plot_partial_fit(x_to_fit, y_to_fit, grad=None, poli=poli):
        """
        Add partial fits to axes.
        """
        xfit, yfit, dyfit = FitData(x_to_fit, y_to_fit,
                                    force=True, grad=grad, type=poli)
        ax1.plot(xfit, yfit, color='r', linestyle='-',
                    linewidth='1.5')
        ax2.plot(xfit, dyfit, color='orange', linewidth='2')

    if data:
        x = [a_data[0] for a_data in data]
        y = [a_data[1] for a_data in data]
    elif not x and not y:
        print 'Must declare either "x" and "y" or two-element set'

    if not sysName:
        sysName = os.path.basename(os.getcwd())


    labels = ['P{0}'.format(i) for i in range(len(x))]
    f0 = plt.figure()
    f0.suptitle(sysName)
    ax0 = f0.add_subplot(111)
    ax0.set_ylabel('y')
    ax0.set_xlabel('x')
    ax0.scatter(x, y, s=50, facecolors='none', edgecolors='red')
    for label, ax, ay in zip(labels, x, y):
        plt.annotate(label, xy=(ax, ay), xytext=(0,20),
                        textcoords='offset points')
    plt.savefig('fit_'+sysName+'.png', format='png', bbox_inches='tight')
    plt.show()

    f2, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
    ax1.set_ylabel('Energy [eV]')
    ax2.set_ylabel('Force [nN]')
    ax2.set_xlabel('Stretching distance [\AA]')
    ax2.axhline(linestyle='--', color='gray', linewidth='2')
    f2.subplots_adjust(hspace=0)
    f2.suptitle(sysName)
    #ax1.scatter(x, y, s=30, facecolors='none', edgecolors='blue')
    ax1.scatter(x, y, s=30, color='blue', alpha=0.4)

    left_x = x
    left_y = y

    while True:
        print 'Range of point numbers? (comma separated):'
        print 'Enter "r"  to fit all remaining points'
        print 'Enter "s"  to stop fitting'

        sel = raw_input('--> ')
        selist = re.split(',|:', sel)

        if selist[0] == 'r':
            if len(selist) == 2:
                grado = int(selist[1])
            else:
                grado = None
            x_to_fit = []
            y_to_fit = []
            for i in range(len(left_x)):
                if re.match(main.patterns['real'], str(left_x[i])):
                    x_to_fit.append(left_x[i])
                    y_to_fit.append(left_y[i])
                    if i == len(left_x) - 1 and len(x_to_fit) > 1:
                        plot_partial_fit(x_to_fit, y_to_fit, grad=grado)
                    elif left_x[i+1] == 'x' and len(x_to_fit) > 1:
                        plot_partial_fit(x_to_fit, y_to_fit, grad=grado)
                        x_to_fit = []
                        y_to_fit = []
            break

        elif selist[0] == 's':
            break
        else:
            a = int(selist[0])
            b = int(selist[1])
            if len(selist) == 3:
                grado = int(selist[2])
            else:
                grado = None
            x_to_fit = x[a:b+1]
            y_to_fit = y[a:b+1]
            left_x = ['x' if i in range(a,b+1) else e for i, e in
                      enumerate(left_x)]
            plot_partial_fit(x_to_fit, y_to_fit, grad=grado)

    plt.savefig(pngOut, format='png', bbox_inches='tight')
    #plt.savefig('energy-force_'+sysName+'.png', format='png',
                #bbox_inches='tight')
    plt.show()

#class File(object):
    #def __init__(self, fname):
def set_file(fname):
    base = os.path.basename(fname)
    if os.path.isfile(fname):
        while True:
            ans = raw_input('File %s already exists. Replace, Append or do Nothing? [R/a/n]'
                    % base)
            ans = ans.lower()
            if ans == 'r':
                f = open(fname, 'w')
                return f
            elif ans == 'a':
                f = open(fname, 'a')
                return f
            elif ans == 'n':
                f = None
                return f
            else:
                print 'Not valid answer.'
    else:
        return open(fname, 'w')


class XSF(object):
    """Internal XCrySDen structure format. XSF stands for XCrySDen Structure
    File. It is used to describe (i) molecular and crystal structure, (ii)
    forces acting on constituent atoms, and (iii) scalar fields (for example:
    charge density, electrostatic potential). The main attributes of XSF
    format are:
        o all records are in free format
        o the XSF formatted file is composed from various sections
        o each sections begins with the keyword
        o there are two types of keywords: (i) single keywords, and (ii)
            sandwich keywords, which are defined as:
                single keyword: section begins with a single keyword and ends
                    without an end-keyword
                sandwich keyword: section begins with a begin-keyword (i.e.
                    BEGIN_keyword) and ends with an end-keyword (i.e.
                    END_keyword), where keyword is one among keywords.
        o all coordinates are in ANGSTROMS units
        o all forces are in Hartree/ANGSTROM units
        o the comment-lines start with the "#" character
    """

    def __init__(self, obj, vec=None):
        if vec:
            self.vec = np.array(vec).reshape(3, 3)
        else:
            self.vec = np.identity(3) * 20
        self._obj = obj

    def readFile(self):
        pass

    def writeToFile(self, fname):
        f = set_file(fname)
        f.write('CRYSTAL\nPRIMEVEC\n')
        np.savetxt(f, self.vec, fmt='%15.5f')
        f.write('PRIMCOORD\n%i 1' % self.obj.atno)

if __name__ == '__main__':
    A = XSF()
    A.writeToFile('salida.dat')
