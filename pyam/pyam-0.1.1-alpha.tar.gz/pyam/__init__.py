"""
Objects imported here will live in the `pyam` namespace

"""
__all__ = ["OrthogonalPolynomialInitialGuess", "Input",
           "AssortativeMatchingModelLike", "AssortativeMatchingProblem"]

from . initial_guesses import OrthogonalPolynomialInitialGuess
from . inputs import Input
from . model import AssortativeMatchingModelLike
from . problem import AssortativeMatchingProblem

# Add Version Attribute
from pkg_resources import get_distribution

__version__ = get_distribution('pyAM').version
