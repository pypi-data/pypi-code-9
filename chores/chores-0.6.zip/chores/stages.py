from chores.core import *

class Stages(object):

    """
    Represent different stages of program operation. (Experimental.)
    """

    def __init__(self, stages=None):
        self.stages = orderedstuf()
        self.open = set()
        self.begin('overall')

    def begin(self, name):
        self.open.add(name)
        if name not in self.stages:
            self.stages[name] = {}
        self.stages[name]['t0'] = time.time()

    def end(self, name):
        self.open.remove(name)
        stageinfo = self.stages[name]
        elapsed = time.time() - stageinfo['t0']
        stageinfo['elapsed'] = stageinfo.get('elapsed', 0) + elapsed
        del stageinfo['t0']

    def enter(self, name):
        return StageContext(self, name)

    def durations(self):
        """
        Return information about duration of each stage.
        """
        dur = orderedstuf()
        for n in list(self.open):
            self.end(n)
        dur.overall = self.stages['overall']['elapsed']
        for name, sinfo in self.stages.items():
            dur[name] = sinfo['elapsed']
        return dur

    def report(self):
        # close everything - is this what we want?
        for n in list(self.open):
            self.end(n)
        text = ""
        overall = self.stages['overall']['elapsed']
        for name, sinfo in self.stages.items():
            elapsed = sinfo['elapsed']
            text += "{0:8} {1:8.3f} {2:>5.1f}%\n".format(name, elapsed, elapsed/overall * 100)
        return text

class StageContext(object):
    def __init__(self, caller, name):
        self.caller = caller
        self.name = name