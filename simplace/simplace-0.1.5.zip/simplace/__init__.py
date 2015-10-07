from .simplace import *

"""
You need Java >= 8.0 and the Simplace simulation framework http://www.simplace.net

To use it do::

    >>> import simplace
    >>> jd = 'd:/java/simplace/'
    >>> wd = 'd:/java/simplace/simplacerun/simulation/'
    >>> od = 'd:/java/simplace/simplacerun/output/'

    >>> sol = wd+'gk/solution/gecros/Gecros.sol.xml'
    >>> proj = wd+'gk/project/gecros/GecrosSensitivityTestNPL.proj.xml'
    
    >>> sh = simplace.initSimplace(jd,wd,od)
    >>> simplace.setProjectLines(sh, [1,3,8,9,17])
    >>> simplace.openProject(sh, sol, proj)
    >>> simplace.runProject(sh)
    >>> simplace.closeProject(sh)

"""