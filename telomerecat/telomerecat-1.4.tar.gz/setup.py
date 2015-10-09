from setuptools import setup,find_packages
from setuptools.command.install import install as _install
from setuptools.command.build_py import build_py
from os.path import join as path_join
import os 
from glob import glob
import platform
import sys
import shutil
import pdb

def _post_install(install_lib,system):
    telomerecat_install_path = path_join(install_lib,"telomerecat")
    linux_bowtie_path = glob(path_join(telomerecat_install_path,"bowtie*linux"))[0]
    macos_bowtie_path = glob(path_join(telomerecat_install_path,"bowtie*macos"))[0]

    if system == "Darwin":
        relevant_binary_path = macos_bowtie_path
        unused_binary_path = linux_bowtie_path
    elif system == "Linux":
        relevant_binary_path = linux_bowtie_path
        unused_binary_path = macos_bowtie_path

    for bowtie_path in os.listdir(relevant_binary_path):
        if "bowtie" in bowtie_path:
            os.chmod(path_join(relevant_binary_path,bowtie_path),0775)
    shutil.rmtree(unused_binary_path)

class install(_install):

    def run(self):
        system = platform.system()
        if not (system == "Darwin" or system == "Linux"):
            print "[ERROR] telomerecat does not function on this operating system!"
            print "\tPlease try again using a Linux or MacOSX based system."
            sys.exit()
        _install.run(self)
        self.execute(_post_install, (self.install_lib,system),
                msg="Selecting and linking correct bowtie2 version for platform")

setup(name='telomerecat',
	  description='Telomere Computational Analysis Tool',
      version='1.4',
      author="JHR Farmery",
      license='GPL',
      cmdclass={'install': install},
      author_email = 'jhrf2@cam.ac.uk',
      packages = ['telomerecat'],
      package_dir = {'telomerecat':'telomerecat'},
      install_requires = ['parabam','argparse','numpy','pysam'],
      include_package_data = True,
      scripts = ['./telomerecat/bin/telomerecat'],
      zip_safe = False
    )
