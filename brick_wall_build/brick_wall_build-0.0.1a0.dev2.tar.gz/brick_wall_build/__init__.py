"""
Lightweight Python Build Tool
"""

__version__ = "0.0.1a.dev2"
__license__ = "MIT License"
__contact__ = "https://github.com/IndeedTokyo-BrickWall/brick-wall-build"
from ._brick_wall_build import task, main
import pkgutil

__path__ = pkgutil.extend_path(__path__,__name__)

__all__ = ["task",  "main"]