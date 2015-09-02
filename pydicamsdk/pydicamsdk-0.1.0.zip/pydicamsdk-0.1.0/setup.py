from setuptools import setup, Extension, find_packages
pcoErrorModule = Extension("pcoError",
                           sources=["pcoError.c"],
                           include_dirs=['C:\Program Files (x86)'
                                         '\Digital Camera Toolbox'
                                         '\Sensicam SDK\include'],
                           define_macros=[("PCO_ERR_H_CREATE_OBJECT", None),
                                          ("PCO_ERRT_H_CREATE_OBJECT", None)],
                           )
setup(
      name="pydicamsdk",
      description="A wrapper for the pco sensicam/dicam SDK",
      version="0.1.0",
      platforms=["win-amd64", 'win32'],
      author="Markus J Schmidt",
      author_email='schmidt@ifd.mavt.ethz.ch',
      license="GNU GPLv3",
      url="https://github.com/smiddy/pydicamsdk",
      packages=find_packages(),
      ext_modules=[pcoErrorModule],
      install_requires=['numpy>=1.9.2', 'Pillow>=2.9.0']
      )
