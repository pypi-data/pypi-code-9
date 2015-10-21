import clr
clr.AddReferenceToFileAndPath("ddiy.dll")

from Clipboard import Clipboard
from WinAPI import WinAPI
from Input import Input
from ImageMatcher import ImageMatcher
from DDIY import Helpers

__version__ = Helpers.GetVersion()
__author__ = "Tomas Bosek - bosektom@gmail.com"
