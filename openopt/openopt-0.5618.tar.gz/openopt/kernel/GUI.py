# sometimes Tkinter is not installed
TkinterIsInstalled = True
import platform#, pylab
from numpy import ndarray
from time import strftime
if platform.python_version()[0] == '2': 
    # Python2
    try:
        from Tkinter import Tk, Text, Toplevel, Button, Entry, Menubutton, Label, Frame, \
        StringVar, DISABLED, ACTIVE, Scrollbar
    except:
        TkinterIsInstalled = False
else: 
    # Python3
    try:
        from tkinter import Tk, Text, Toplevel, Button, Entry, Menubutton, Label, Frame, \
        StringVar, DISABLED, ACTIVE, Scrollbar
    except:
        TkinterIsInstalled = False


from threading import Thread
from openopt import __version__ as ooversion
from setDefaultIterFuncs import BUTTON_ENOUGH_HAS_BEEN_PRESSED, USER_DEMAND_EXIT
from ooMisc import killThread
#from runProbSolver import finalShow

def manage(p, *args, **kwargs):
    bg_color = p._bg_color = '#FFFFF0'
    p.isManagerUsed = True
    if not TkinterIsInstalled: 
        p.err('''
        Tkinter is not installed. 
        If you have Linux you could try using "apt-get install python-tk"
        ''')
    # expected args are (solver, start) or (start, solver) or one of them
    p._args = args
    p._kwargs = kwargs
    

    for arg in args:
        if type(arg) == str or hasattr(arg, '__name__'): 
            p.solver = arg
        elif arg in (0, 1, True, False): 
            start = arg
        else: 
            p.err('Incorrect argument for manage()')

    start = kwargs.pop('start', True)

    if 'solver' in kwargs: 
        p.solver = kwargs['solver']

    # root

    root = Tk()
    p.GUI_root = root

    F0 = Frame(root)
    F0_side = 'right'
    textSide = 'left'
    if p.managerTextOutput is not False:
        F_text = Frame(root)
        scrollbar = Scrollbar(F_text)
        scrollbar.pack(side='right', fill='y')
        
        textOutput = Text(F_text, yscrollcommand=scrollbar.set, bg=bg_color)
        
        p._setTextFuncs()
        for func in ('warn', 'err', 'info', 'disp', 'hint', 'pWarn'):
            setattr(p, func, updated_output(getattr(p, func), textOutput))
        
        if p.managerTextOutput in ('right', 'left'):
            textSide = p.managerTextOutput
            if p.managerTextOutput == 'right': 
                F0_side = 'left'
        
        textOutput.pack(expand=True, fill='both')
        F_text.pack(side=textSide, fill='both', expand=True)
        
        scrollbar.config(command=textOutput.yview)
        
    F0.pack(side=F0_side)
    
    # Title
    #root.wm_title('OpenOpt  ' + ooversion)


    p.GUI_items = {}

    """                                              Buttons                                               """

    # OpenOpt label
    Frame(F0).pack(ipady=4, expand=True)
    Label(F0, text=' OpenOpt ' + ooversion + ' ').pack(expand=True, fill='x')
    Label(F0, text=' Solver: ' + (p.solver if isinstance(p.solver, str) else p.solver.__name__) + ' ').pack(expand=True, fill='x')
    Label(F0, text=' Problem: ' + p.name + ' ').pack(expand=True, fill='x')
    #TODO: use Menubutton 


    #Statistics
#    stat = StringVar()
#    stat.set('')
#    Statistics = Button(F0, textvariable = stat, command = lambda: invokeStatistics(p))

#    cw = Entry(F0)
#
#    
#    b = Button(F0, text = 'Evaluate!', command = lambda: invokeCommand(cw))
#    cw.pack(fill='x'', side='left')
#    b.pack(side='right')
        
    # Run
    t = StringVar()
    t.set("      Run      ")
    RunPause = Button(F0, textvariable = t, command = lambda: invokeRunPause(p))
    Frame(F0).pack(ipady=8, expand=True, fill='x')
    RunPause.pack(ipady=15, expand=True, fill='x')
    p.GUI_items['RunPause'] = RunPause
    p.statusTextVariable = t


    # Enough
    def invokeEnough():
        p.userStop = True
        p.istop = BUTTON_ENOUGH_HAS_BEEN_PRESSED
        if hasattr(p, 'stopdict'):  
            p.stopdict[BUTTON_ENOUGH_HAS_BEEN_PRESSED] = True
        p.msg = 'button Enough has been pressed'

        if p.state == 'paused':
            invokeRunPause(p, isEnough=True)
        else:
            RunPause.config(state=DISABLED)
            Enough.config(state=DISABLED)
            Quit.config(state=DISABLED)
    Frame(F0).pack(ipady=8, expand=True, fill='x')
    Enough = Button(F0, text = '   Enough!   ', command = invokeEnough)
    Enough.config(state=DISABLED)
    Enough.pack(expand=True, fill='x')
    p.GUI_items['Enough'] = Enough


    '''                             Result                         '''
    
    Result = Button(F0, text = '   Result   ', command = lambda: invokeResult(p))
    Result.config(state=DISABLED)
    # TODO: MOP
    if p.probType in ('NLP', 'SNLE', 'NLSP', 'GLP', 'LP', 'MILP', 'NSP', 'MINLP') \
    or p.probType.endswith('QP'):
        Frame(F0).pack(ipady=8, expand=True, fill='x')
        Result.pack(expand=True, fill='x')
    p.GUI_items['Result'] = Result

    '''                             Exit                         '''

    Frame(F0).pack(ipady=8, expand=True, fill='x')
    Quit = Button(F0, text="      Exit      ", command = lambda:invokeExit(p))
    Quit.pack(ipady=15, expand=True, fill='x')
    p.GUI_items['Quit'] = Quit
    
    '''                             Time                         '''
    Frame(F0).pack(ipady=0, expand=True, fill='x')
    F = Frame(F0)
    _time = StringVar()
    p._manager_time = 0
    p._manager_time_variable = _time
    Label(F, text=" Time:\t\t").pack(side='left', expand=True, fill='x')
    _time.set("%d" % p._manager_time)
    _Time = Label(F, textvariable = _time)
    _Time.pack(side='right', ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['time'] = _time
    F.pack(ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    
    '''                         CPU Time                         '''
    Frame(F0).pack(ipady=0, expand=True, fill='x')
    F = Frame(F0)
    _cputime = StringVar()
    p._manager_cputime = 0
    _cputime.set(p._manager_cputime)
    p._manager_cputime_variable = _cputime
    Label(F, text=" CPU Time:\t").pack(side='left', expand=True, fill='x')
    _time.set("%d" % p._manager_cputime)
    _CPUTime = Label(F, textvariable = _cputime)
    _CPUTime.pack(side='right', ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['cputime'] = _cputime
    F.pack(ipady=1, ipadx=3, padx=3, expand=True, fill='x')


    """                                            Start main loop                                      """
    #state = 'paused'

    if start:
        Thread(target=invokeRunPause, args=(p, )).start()
    root.mainloop()
    #finalShow(p)


    """                                              Handle result                                       """

    if hasattr(p, 'tmp_result'):
        r = p.tmp_result
        delattr(p, 'tmp_result')
    else:
        r = None


    """                                                    Return                                           """
    return r
    
########################################################


def invokeRunPause(p, isEnough=False):
    try:
        import pylab
    except:
        if p.plot: 
            p.warn('to use graphics you should have matplotlib installed')
            p.plot = False
        
    if isEnough:
        p.GUI_items['RunPause'].config(state=DISABLED)

    if p.state == 'init':
        p.probThread = Thread(target=doCalculations, args=(p, ))
        p.state = 'running'
        p.statusTextVariable.set('    Pause    ')
        p.GUI_items['Enough'].config(state=ACTIVE)
        p.GUI_root.update_idletasks()
        p.probThread.start()

    elif p.state == 'running':
        p.state = 'paused'
        if p.plot: 
            pylab.ioff()
        p.statusTextVariable.set('      Run      ')
        p.GUI_root.update_idletasks()

    elif p.state == 'paused':
        p.state = 'running'
        if p.plot:
            pylab.ion()
        p.statusTextVariable.set('    Pause    ')
        p.GUI_root.update_idletasks()

def doCalculations(p):
    try:
        p.tmp_result = p.solve(*p._args, **p._kwargs)
        p.GUI_items['Result'].config(state='active')
    except killThread:
        if p.plot:
            if hasattr(p, 'figure'):
                #p.figure.canvas.draw_drawable = lambda: None
                try:
                    import pylab
                    pylab.ioff()
                    pylab.close('all')
                except:
                    pass


#def invokeStatistics(p):
def invokeCommand(cw):
    exec(cw.get())

def updated_output(func, textOutput):
    def func2(msg):
        msgCap = func.s 
        Set = getattr(func, 'set', ())
        if msg in Set:
            return
        if msgCap == 'OpenOpt Error: ': #if type(Set) != tuple:
            textOutput.tag_config(msg, foreground="red")
            textOutput.config(foreground="red")
        textOutput.insert('end', msgCap + msg + '\n')
        textOutput.yview('end')
        func(msg)
    return func2

def invokeResult(p):
    #TODO: deiconify if exists
    r = p.tmp_result
    T = Toplevel(p.GUI_root)
    
    C = Frame(T)
    C.pack(side='bottom', fill='x', expand=True)
    E = Button(C, text="      Close      ", command = T.destroy)
    E.pack(ipady=15, expand=True, fill='x')
    
    R = Text(T, bg=p._bg_color)
    R.pack(side = 'left', expand=True, fill='both')
    scrollbar = Scrollbar(T)
    scrollbar.pack(side='right', fill='y')

    if r is None:
        R.insert('end', 'result is None, no other info is available')
        return
    R.insert('end', 'Name: ' +  p.name + '\n')
    R.insert('end', 'Type: ' +  p.probType + '\n')
    R.insert('end', 'Solver: ' +  p.solver.__name__ + '\n')
#        R.highlight_pattern("word", foreground="red")
    R.insert('end', strftime("Started: \t%a, %d %b %Y %H:%M:%S\n", p._localtime_started))
    R.insert('end', strftime("Finished:\t%a, %d %b %Y %H:%M:%S\n", p._localtime_finished))
    
    if p.isObjFunValueASingleNumber:
        R.insert('end', 'Objective value: %0.9g' %  p.ff + '\n')
        if 'extremumBounds' in r.extras:
            t = r.extras['extremumBounds']
            R.insert('end', 'Estimated |f - f*|: %0.2g' % (t[1]-t[0])+ '\n')
    
    for fn in ('isFeasible', 'stopcase','istop', 'msg'):
        R.insert('end', fn +': ' + str(getattr(r, fn)) + '\n')
    
    #R.insert('end', '-'*15+'variables'+'-'*15+ '\n')
    R.insert('end', '-'*45+'\n')
    if p.isFDmodel:
        from FuncDesigner import _Stochastic
        '''                                           Free vars                                                         '''
        usedVars = set()
        rr = []
        free_ooarrays = p._init_ooarrays.difference(p._init_fixed_ooarrays)
        for v in free_ooarrays:
            if v.name.startswith('unnamed') and not v[0].name.startswith('unnamed'):
                for _v in v.view(ndarray):
                    if isinstance(_v(r), _Stochastic): continue
                    rr.append(_v.name +': ' + str(_v(r)))
            else:
                if isinstance(v[0](r), _Stochastic): continue #TODO: check other array elements
                rr.append(v.name +': ' + str(v(r).tolist()))
            usedVars.update(v.view(ndarray).tolist())
        for v in p.freeVarsSet.difference(usedVars):
            V = v(r)
            if isinstance(V, _Stochastic): continue
            rr.append(v.name +': ' + str(V if type(V)!=ndarray else V.tolist()))
        rr.sort(key = lambda elem:len(elem))
        for elem in rr:
            R.insert('end', elem + '\n')
        '''                                           Fixed vars                                                         '''
        
        if len(p.fixedVarsSet) != 0:
            usedVars = set()
            rr = []
            fixed_ooarrays = p._init_fixed_ooarrays
            for v in fixed_ooarrays:
                if v.name.startswith('unnamed') and not v[0].name.startswith('unnamed'):
                    for _v in v.view(ndarray):
                        if isinstance(_v(r), _Stochastic): continue
                        rr.append(_v.name +': ' + str(_v(r)))
                else:
                    if isinstance(v[0](r), _Stochastic): continue#TODO: check other array elements
                    rr.append(v.name +': ' + str(v(r).tolist()))
                usedVars.update(v.view(ndarray).tolist())
            for v in p.fixedVarsSet.difference(usedVars):
                V = v(r)
                if isinstance(V, _Stochastic): continue
                rr.append(v.name +': ' + str(V if type(V)!=ndarray else V.tolist()))
            rr.sort(key = lambda elem:len(elem))
            if len(rr):
                R.insert('end', '\n'+'-'*13+'  fixed variables  ' + '-'*13 + '\n')
                for elem in rr:
                    R.insert('end', elem + '\n')
    else:
        R.insert('end', str(r.xf) + '\n')



def invokeExit(p):
        p.userStop = True
        p.istop = USER_DEMAND_EXIT
        if hasattr(p, 'stopdict'): 
            p.stopdict[USER_DEMAND_EXIT] = True

        # however, the message is currently unused
        # since openopt return r = None
        p.msg = 'user pressed Exit button'

        p.GUI_root.destroy()
