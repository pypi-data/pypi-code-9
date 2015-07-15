from oologfcn import OpenOptException
from numpy import ndarray, matrix, asscalar, asarray, asfarray
from time import time, clock

class OpenOptResult: 
    # TODO: implement it
    #extras = EmptyClass() # used for some optional output
    def __call__(self, *args):
        if not self.isFDmodel:
            raise OpenOptException('Is callable for FuncDesigner models only')
        r = []
        for arg in args:
            tmp = [(self._xf[elem] if isinstance(elem,  str) \
                    else self.xf[elem]) for elem in (arg.tolist() if isinstance(arg, ndarray) \
                    else arg if type(arg) in (tuple, list) else [arg])]
            tmp = [asscalar(item) if type(item) in (ndarray, matrix) and item.size == 1 \
                   #else item[0] if type(item) in (list, tuple) and len(item) == 0 \
                   else item for item in tmp]
            r.append(tmp if type(tmp) not in (list, tuple) or len(tmp)!=1 else tmp[0])
        r = r[0] if len(args) == 1 else r
        if len(args) == 1 and type(r) in (list, tuple) and len(r) >1: r = asfarray(r, dtype = type(r[0]))
        return r
        
    def __init__(self, p):
        self.rf = asscalar(asarray(p.rf))
        self.ff = asscalar(asarray(p.ff))
        self.isFDmodel = p.isFDmodel
        self.probType = p.probType
        if p.probType == 'EIG':
            self.eigenvalues, self.eigenvectors = p.eigenvalues, p.eigenvectors
        
        if p.isFDmodel:
            from FuncDesigner import oopoint
            self.xf = dict((v, asscalar(val) if isinstance(val, ndarray) and val.size ==1 \
                            else dict((field, v.domain[int(val)][j]) for j, field in enumerate(v.fields)) if v.fields != ()\
                            else v.reverse_aux_domain[int(val)] if 'reverse_aux_domain' in v.__dict__\
                            else v.aux_domain[val] if 'aux_domain' in v.__dict__ else val) \
                            for v, val in p.xf.items())
            if not hasattr(self, '_xf'):
                #self._xf = dict([(v.name, asscalar(val) if isinstance(val, ndarray) and val.size ==1 else val) for v, val in p.xf.items()])
                self._xf = dict((v.name, val) for v, val in self.xf.items())
            self.xf = oopoint(self.xf, maxDistributionSize = p.maxDistributionSize, skipArrayCast = True)
        else:
            self.xf = p.xf
        
        # TODO: mb use the fields in MOP
        if p.probType == 'MOP':
            for attr in ('xf', 'ff', 'rf', '_xf'):
                delattr(self, attr)

        
        #if len(p.solutions) == 0 and p.isFeas(p.xk): p.solutions = [p.xk]
        
        # TODO: mb perform check on each solution for more safety?
        # although it can slow down calculations for huge solutions number
        #self.solutions = p.solutions 

        self.elapsed = dict()
        self.elapsed['solver_time'] = round(100.0*(time() - p.timeStart))/100.0
        self.elapsed['solver_cputime'] = round(100.0*(clock() - p.cpuTimeStart))/100.0
        self.elapsed['initialization_time'] = round(100.0*p.initTime)/100.0
        self.elapsed['initialization_cputime'] = round(100.0*p.initCPUTime)/100.0

        for fn in ('ff', 'istop', 'duals', 'isFeasible', 'msg', 'stopcase', 'iterValues',  'special', 'extras', 'solutions'):
            if hasattr(p, fn):  setattr(self, fn, getattr(p, fn))

        if hasattr(p.solver, 'innerState'):
            self.extras['innerState'] = p.solver.innerState

        self.solverInfo = dict()
        for fn in ('homepage',  'alg',  'authors',  'license',  'info', 'name'):
            self.solverInfo[fn] =  getattr(p.solver,  '__' + fn + '__')

            # note - it doesn't work for len(args)>1 for current Python ver  2.6
            #self.__getitem__ = c # = self.__call__
            
        if p.plot:
            #for df in p.graphics.drawFuncs: df(p)    #TODO: include time spent here to (/cpu)timeElapsedForPlotting
            self.elapsed['plot_time'] = round(100*p.timeElapsedForPlotting[-1])/100 # seconds
            self.elapsed['plot_cputime'] = p.cpuTimeElapsedForPlotting[-1]
        else:
            self.elapsed['plot_time'] = 0
            self.elapsed['plot_cputime'] = 0

        self.elapsed['solver_time'] -= self.elapsed['plot_time']
        self.elapsed['solver_cputime'] -= self.elapsed['plot_cputime']

        self.evals = dict([(key, val if type(val) == int else round(val *10) /10.0) for key, val in p.nEvals.items()])
        self.evals['iter'] = p.iter
        

