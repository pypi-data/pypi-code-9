"""
Lightweight Python Build Tool
"""

__version__ = "0.0.1a.dev3"
__license__ = "MIT License"
__contact__ = "https://github.com/IndeedTokyo-BrickWall/brick-wall-build"
from ._brick_wall_build import task, main, set_artifact_path, set_tmp_path, run
import pkgutil

__path__ = pkgutil.extend_path(__path__,__name__)

__all__ = ["task",  "main", "set_artifact_path", "set_tmp_path", "run"]