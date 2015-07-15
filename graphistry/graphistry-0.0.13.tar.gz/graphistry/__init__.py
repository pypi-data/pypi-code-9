from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('graphistry').version
except DistributionNotFound:
    __version__ = '0.0.0'

from graphistry.etl import settings, plot
