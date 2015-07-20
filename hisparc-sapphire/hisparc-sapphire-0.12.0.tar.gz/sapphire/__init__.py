"""Simulation and Analysis Program Package for HiSPARC Research

SAPPHiRE simplifies data access, simulations and analysis for the
`HiSPARC <http://www.hisparc.nl>`_ experiment.  It was born out of a
combination of the old framework and the collection of simulation and
analysis scripts developed by David Fokkema for his PhD thesis work.

The following packages and modules are included:

:mod:`~sapphire.analysis`
    package containing analysis-related modules

:mod:`~sapphire.api`
    publicdb api interface

:mod:`~sapphire.clusters`
    definitions for HiSPARC detectors, stations and clusters

:mod:`~sapphire.corsika`
    package containing CORSIKA simulation related modules

:mod:`~sapphire.esd`
    event summary data access

:mod:`~sapphire.kascade`
    work on KASCADE data

:mod:`~sapphire.publicdb`
    public data access

:mod:`~sapphire.simulations`
    package containing simulation-related modules

:mod:`~sapphire.storage`
    storage-related definitions

:mod:`~sapphire.time_util`
    GPS date/time utility functions

:mod:`~sapphire.transformations`
    transformations between different systems

:mod:`~sapphire.utils`
    commonly used functions such as a progressbar

"""
from . import analysis
from . import api
from . import clusters
from . import corsika
from . import esd
from . import kascade
from . import publicdb
from . import simulations
from . import storage
from . import time_util
from . import transformations
from . import utils

from .analysis.coincidence_queries import CoincidenceQuery
from .analysis.coincidences import Coincidences, CoincidencesESD
from .analysis.find_mpv import FindMostProbableValueInSpectrum
from .analysis.process_events import (ProcessEvents, ProcessEventsFromSource,
                                      ProcessEventsFromSourceWithTriggerOffset,
                                      ProcessWeather, ProcessWeatherFromSource)
from .analysis.reconstructions import (ReconstructESDEvents,
                                       ReconstructESDCoincidences)
from .api import Network, Station
from .clusters import HiSPARCStations, HiSPARCNetwork, ScienceParkCluster
from .esd import (quick_download, load_data, download_data,
                  download_coincidences)
from .simulations.groundparticles import GroundParticlesSimulation
from .simulations.ldf import KascadeLdfSimulation, NkgLdfSimulation
from .simulations.showerfront import FlatFrontSimulation, ConeFrontSimulation
from .transformations.celestial import zenithazimuth_to_equatorial


__all__ = ['analysis',
           'api',
           'clusters',
           'corsika',
           'esd',
           'kascade',
           'publicdb',
           'simulations',
           'storage',
           'time_util',
           'transformations',
           'utils',
           'CoincidenceQuery',
           'Coincidences', 'CoincidencesESD',
           'FindMostProbableValueInSpectrum',
           'ProcessEvents', 'ProcessEventsFromSource',
           'ProcessEventsFromSourceWithTriggerOffset',
           'ProcessWeather', 'ProcessWeatherFromSource',
           'ReconstructESDEvents', 'ReconstructESDCoincidences',
           'Network', 'Station',
           'HiSPARCStations', 'HiSPARCNetwork', 'ScienceParkCluster',
           'quick_download', 'load_data', 'download_data',
           'download_coincidences',
           'GroundParticlesSimulation',
           'KascadeLdfSimulation', 'NkgLdfSimulation',
           'FlatFrontSimulation', 'ConeFrontSimulation',
           'zenithazimuth_to_equatorial'
           ]
