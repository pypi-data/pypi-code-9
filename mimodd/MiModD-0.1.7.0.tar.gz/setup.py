import os
import sys
import glob
import shutil
import hashlib
import re
import fnmatch
import stat
import platform
import subprocess

assert sys.version_info[:2] >= (3,2), 'MiModD requires Pyhon3.2 +'

# detect injection of setuptools (presumably) by pip
SETUPTOOLS_INJECTED = 'setuptools' in sys.modules

try:
    # enable installation via setuptools
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from distutils.command.build import build as _build
from distutils.command.install_lib import install_lib as _install_lib
from distutils.command.clean import clean as _clean

                     
VERSION = '0.1.7.0'
SNAP_SOURCE = os.path.abspath('snap')
SAMTOOLS_SOURCES = os.path.abspath('pysam')
SAMTOOLS_LEGACY = os.path.join(SAMTOOLS_SOURCES, 'samtools')
SAMTOOLS_1_0 = os.path.join(SAMTOOLS_SOURCES, 'samtools-1.x')
BCFTOOLS_1_0 = os.path.join(SAMTOOLS_SOURCES, 'bcftools-1.x')
HTSLIB_1_0 = os.path.join(SAMTOOLS_SOURCES, 'htslib-1.x')
SCRIPTS = os.path.abspath('scr')
GALAXY_WRAPPERS = os.path.abspath('lib/MiModD/galaxy_data/mimodd')
EXECUTABLES_TMP_DEST = os.path.join(os.path.abspath('lib'), 'MiModD' , 'bin')
EXECUTABLES = ['samtools', 'bcftools', 'snap', 'samtools_legacy', 'mimodd']

LOG_FILE = os.path.abspath('setup.log')


class MiModDInstallationError (RuntimeError):
    pass


def _print (*args, **kwargs):
    # an unbuffered version of print for real-time status messages from pip
    stream = kwargs.get('file') or sys.stdout
    print(*args, **kwargs)
    stream.flush()


# from the pysam installer
def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
       for filename in fnmatch.filter(files, pattern):
          yield os.path.join(path, filename)
    

def prepare_package ():
    with open(LOG_FILE, 'a') as log:
        print('Preparing to install MiModD v{0}.'.format(VERSION))
        print()
        if not os.path.isdir(EXECUTABLES_TMP_DEST):
            os.mkdir(EXECUTABLES_TMP_DEST)
            
        # compile samtools, bcftools and snap from source
        # if their binaries do not exist already
        for sourcedir, command, toolname in zip(
            (HTSLIB_1_0, SAMTOOLS_1_0, BCFTOOLS_1_0,
             SAMTOOLS_LEGACY, SNAP_SOURCE),
            (['make'], ['make', 'HTSDIR=' + HTSLIB_1_0],
             ['make', 'HTSDIR=' + HTSLIB_1_0], ['make'], ['make']), 
            ('htslib', 'samtools', 'bcftools', 'legacy samtools (v0.1.19)',
             'snap')):
            print('Building {0} ..'.format(toolname), end = ' ')
            p = subprocess.Popen(
                command, cwd=sourcedir, stdout=log, stderr=log)
            if p.wait():
                print('FAILED!')
                raise MiModDInstallationError(
                    'Building step failed. Aborting.')
            else:
                print('Succeeded.')
                
        # copy all binaries to a temporary 'bin' directory to include 
        # in the build         
        shutil.copy(os.path.join(SAMTOOLS_1_0, 'samtools'),
                    EXECUTABLES_TMP_DEST)
        shutil.copy(os.path.join(BCFTOOLS_1_0, 'bcftools'),
                    EXECUTABLES_TMP_DEST)
        shutil.copy(os.path.join(SAMTOOLS_LEGACY, 'samtools'),
                    os.path.join(EXECUTABLES_TMP_DEST, 'samtools_legacy'))
        shutil.copy(os.path.join(SNAP_SOURCE, 'snap'), EXECUTABLES_TMP_DEST)

        print('All source compilation successful.')
        
        ########## prepare pysam part of installation ##############
        # modified from pysam's setup.py
        # redirect stderr to pysamerr and replace bam.h with a stub.
        print('Preparing pysam for building ..', end=' ')        
        SAMTOOLS_EXCLUDE = ("bamtk.c", "razip.c", "bgzip.c", 
                     "main.c", "calDepth.c", "bam2bed.c",
                     "wgsim.c", "md5fa.c", "maq2sam.c",
                     "bamcheck.c",
                     "chk_indel.c")
        cf = locate('*.c', SAMTOOLS_LEGACY)
        for filename in cf:
            if os.path.basename(filename) in SAMTOOLS_EXCLUDE: continue
            if not filename or filename.endswith('.pysam.c'): continue
            dest = filename + '.pysam.c'
            if not os.path.exists(dest):
                with open(filename) as infile:
                    with open(dest, 'w') as outfile:
                        outfile.write('#include "pysam.h"\n\n')
                        outfile.write(
                            re.sub('stderr', 'pysamerr',
                                   ''.join(infile.readlines())))
        pysam_h_file = os.path.join(SAMTOOLS_LEGACY, "pysam.h")
        if not os.path.exists(pysam_h_file):
            with open(pysam_h_file, "w") as outfile:
                outfile.write(
"""#ifndef PYSAM_H
#define PYSAM_H
#include "stdio.h"
extern FILE * pysamerr;
#endif
""")
        # add the newly created files to the list of samtools Extension
        # source files
        samtools.sources += glob.glob(
            os.path.join(SAMTOOLS_LEGACY, "*.pysam.c")) + glob.glob(
            os.path.join(SAMTOOLS_LEGACY, "*", "*.pysam.c"))

        print('Succeeded.')
        
        # add version tag to galaxy tool wrappers
        for wrapper in os.listdir(GALAXY_WRAPPERS):
            with open(os.path.join(GALAXY_WRAPPERS,
                                    wrapper), 'r') as wrapper_in:
                first_line = wrapper_in.readline()
                if not 'version="x.x"' in first_line:
                    raise RuntimeError(
                        'Compromised tool identifier line in Galaxy tool wrapper file {0}'
                        .format(wrapper)
                        )
                first_line = first_line.replace('version="x.x"',
                                                'version="{0}"'.format(VERSION))
                remaining_lines = wrapper_in.readlines()
            with open(os.path.join(GALAXY_WRAPPERS,
                                    wrapper), 'w') as wrapper_out:
                wrapper_out.write(first_line)
                wrapper_out.writelines(remaining_lines)

        # Copy mimodd main script to bin to have it available even
        # if installation as a script fails (this can happen with
        # wheel files and when using the upgrade tool).
        shutil.copy(os.path.join(SCRIPTS, 'mimodd'), EXECUTABLES_TMP_DEST)


class build(_build):
    """MiModD custom source builder."""
    
    # Prepares all required binaries of wrapped software and
    # the modified samtools C files required by pysam before 
    # calling the standard build.

    def run (self):
        try:
            prepare_package() # do C compilations and modifications here
            
            print('Building pysam and assembling installation components ..',
                  end=' ')
            with open(LOG_FILE, 'a') as log: 

                # call distutil's standard build command class
                # to do the rest of the work
                # but redirect its output (mostly compiler messages)
                # to the log file
                oldstdout = oldstderr = None
                try:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    oldstdout = os.dup(sys.stdout.fileno())
                    oldstderr = os.dup(sys.stderr.fileno())
                    os.dup2(log.fileno(), sys.stdout.fileno())
                    os.dup2(log.fileno(), sys.stderr.fileno())
                    _build.run (self)
                except:
                    raise MiModDInstallationError('Failed. Aborting.')
                finally:
                    if oldstdout is not None:
                        os.dup2(oldstdout, sys.stdout.fileno())
                    if oldstderr is not None:
                        os.dup2(oldstderr, sys.stderr.fileno())
            print('Succeeded.')

        finally:
            print('Tidying up ..', end=' ')
            # Remove temporary binaries.
            # We may not have permission do to this in a separate
            # setup.py clean run.
            try:
                shutil.rmtree(EXECUTABLES_TMP_DEST)
            except:
                pass
            print('Done')
            
        print()
        print('MiModD build process finished successfully !')


class install_lib (_install_lib):
    def run (self):
        _install_lib.run(self)
        # make MiModD binaries executable by everyone
        permissions = stat.S_IRWXU | stat.S_IRGRP | \
                      stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
        for fn in self.get_outputs():
            if os.path.basename(fn) in EXECUTABLES:
                os.chmod(fn, permissions)


class clean (_clean):
    """MiModD custom source distribution cleaner."""
    
    # Calls the standard clean to delete files in the build directory
    # but also removes all temporary files generated by the custom build
    # in other directories
    
    def run (self):
        _clean.run(self)
        # remove pysam.c files
        print('Discarding all precompiled components ..', end=' ')
        pysamcfiles = locate("*.pysam.c", SAMTOOLS_LEGACY)
        for f in pysamcfiles:
            try:
                os.remove(f)
            except OSError:
                pass
                
        # clear source directories of wrapped software
        with open(LOG_FILE, 'a') as log:
            for sourcedir, options in zip(
                (HTSLIB_1_0,
                 SAMTOOLS_1_0,
                 BCFTOOLS_1_0,
                 SAMTOOLS_LEGACY,
                 SNAP_SOURCE),
                ([],
                 ['HTSDIR=' + HTSLIB_1_0],
                 ['HTSDIR=' + HTSLIB_1_0],
                 [],
                 [])):
                p = subprocess.Popen(
                    ['make', 'clean'] + options,
                    cwd=sourcedir, stdout=log, stderr=log)
                if p.wait():
                    print(
                    'Warning: Could not remove all temporary files from {0}.'
                    .format(sourcedir))
        print('Done.')
        print('Resetting log file ..', end=' ')
        with open(LOG_FILE, 'w') as log:
            pass
        print('Done.')


#######################################################
# Calling the setup function

# register the custom command classes defined above
cmdclass = {'build': build,
            'install_lib': install_lib,
            'clean': clean}

csamtools_sources = [ "pysam/pysam/csamtools.c" ]

# creating the samtools Extension for pysam
samtools = Extension(
    "MiModD.pysam.csamtools",              
    csamtools_sources + ["pysam/pysam/%s" % x for x in ("pysam_util.c", )], 
    library_dirs=[],
    include_dirs=[SAMTOOLS_LEGACY, "pysam/pysam" ],
    libraries=[ "z", ],
    language="c",
    # pysam code is not ISO-C90 compliant,
    #so ensure it compiles independently of default compiler flags.
    extra_compile_args=["-Wno-error=declaration-after-statement"],
    define_macros = [('_FILE_OFFSET_BITS','64'),
                     ('_USE_KNETFILE','')], 
    )

with open('README.txt') as file:
    long_description = file.read()

if __name__ == '__main__':
    # let's set things up !
    try:    
        setup(name = 'MiModD',
              cmdclass = cmdclass,
              version = VERSION,
              description = 'Tools for Mutation Identification in Model Organism Genomes using Desktop PCs',
              author = 'Wolfgang Maier',
              author_email = 'wolfgang.maier@biologie.uni-freiburg.de',
              url = 'http://sourceforge.net/projects/mimodd/',
              download_url = 'http://sourceforge.net/projects/mimodd/',
              license = 'GPL',
              packages = ['MiModD',
                          'MiModD.pysam',
                          'MiModD.pysam.include',
                          'MiModD.pysam.include.samtools',
                          'MiModD.pysam.include.samtools.bcftools'],
              package_dir = {'': 'lib',
                             'MiModD.pysam': 'pysam/pysam',
                             'MiModD.pysam.include.samtools':'pysam/samtools'},
              package_data = {'' :['bin/*',
                                   'galaxy_data/*.xml',
                                   'galaxy_data/mimodd/*.xml'],
                              'MiModD.pysam' : ['*.pxd', '*.h']},
              scripts = ['scr/mimodd'],
              classifiers=[
                  'Development Status :: 5 - Production/Stable',
                  'Environment :: Console',
                  'Environment :: Web Environment',
                  'Intended Audience :: End Users/Desktop',
                  'Intended Audience :: Developers',
                  'Intended Audience :: Science/Research',
                  'License :: OSI Approved :: GNU General Public License (GPL)',
                  'Operating System :: MacOS :: MacOS X',
                  'Operating System :: POSIX',
                  'Operating System :: POSIX :: Linux',
                  'Operating System :: Unix',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.2',
                  'Programming Language :: Python :: 3.3',
                  'Programming Language :: Python :: 3.4',
                  'Natural Language :: English',
                  'Topic :: Scientific/Engineering',
                  'Topic :: Scientific/Engineering :: Bio-Informatics'],
              ext_modules = [samtools],
              long_description = long_description
              )
    except MiModDInstallationError as error:
        print(error.args[0])
        print()
        try:
            with open(LOG_FILE, 'r') as logged:
                print('Displaying end of installation log file for debugging:')
                print()
                lines = logged.readlines()
            for line in lines[-15:]:
                print(line, end = '')
            print()
            if not SETUPTOOLS_INJECTED:
                print('Display full log file ({0} lines) [y/n]? '
                      .format(len(lines)))
                ans = input()
                if ans == 'y' or ans == 'Y':
                    print()
                for line in lines:
                    print(line, end = '')
                print()
        except (IOError, OSError):
            pass
        sys.exit(1)

    if SETUPTOOLS_INJECTED and 'egg_info' in sys.argv:
        # right before a pip call of the egg_info command finishes
        # is the best place to emit a last message about the build
        # process, which prevents communication
        print("""


Going to build the MiModD package.

This may take a few minutes during which pip may not display live status
information.

Just hang on ..


""")
