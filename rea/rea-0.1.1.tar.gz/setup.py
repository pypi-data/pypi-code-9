from numpy.distutils.core import setup, Extension

setup(name="rea",
      version="0.1.1",
      author="Alexandre Beelen",
      author_email="alexandre.beelen@ias.u-psud.fr",

      url="http://www.ias.u-psud.fr/abeelen/rea",
      download_url = "http://www.ias.u-psud.fr/abeelen/rea/download",
      description="REceiver Array Analysis software",

      classifiers = [
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
          "Environment :: X11 Applications",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Programming Language :: Fortran",
          "Topic :: Scientific/Engineering :: Astronomy",
          ],
      packages=["rea", "rea.Bogli", "rea.fortran"],
      package_data={'rea.Bogli': ['lut/*.lut']},
      scripts=['bin/rea'],

      package_dir={'rea': '.',
                   'rea.Bogli': 'Bogli',
                   'rea.fortran': 'fortran'},
      ext_modules=[
          Extension(
              'rea.fortran.fBaseline',
              ['fortran/fBaseline.f90', 'fortran/fFit.f90'],
              extra_link_args=['-llapack -lblas']),
          Extension(
              'rea.fortran.fFit',
              ['fortran/fFit.f90'],
              extra_link_args=['-llapack -lblas']),
          Extension(
              'rea.fortran.fFlagHandler',
              ['fortran/fFlagHandler.f90']),
          Extension(
              'rea.fortran.fFlag',
              ['fortran/fFlag.f90']),
          Extension(
              'rea.fortran.fMap',
              ['fortran/fMap.f90'],
              extra_link_args=['-llapack -lblas']),
          Extension(
              'rea.fortran.fSNF',
              ['fortran/fSNF.f90', 'fortran/fFit.f90'],
              extra_link_args=['-llapack -lblas']),
          Extension(
              'rea.fortran.fStat',
              ['fortran/fStat.f90']),
          Extension(
              'rea.fortran.fUtilities',
              ['fortran/fUtilities.f90']),
          Extension(
              'rea.fortran.fWavelets',
              ['fortran/fWavelets.f90'])
      ],



)
