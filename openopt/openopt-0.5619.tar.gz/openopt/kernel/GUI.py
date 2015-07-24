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

    if not TkinterIsInstalled: 
        p.err('''
        Tkinter is not installed. 
        If you have Linux you could try using "apt-get install python-tk"
        ''')
        
    p._immutable = False
    bg_color = p._bg_color = '#FFFFF0'
    p.isManagerUsed = True
    
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
    p.GUI_items = {}

    F0 = Frame(root)
    F0_side = 'right'
    textSide = 'left'
    
    F_side = Frame(root)
    p.GUI_items['F_side'] = F_side

    
    F_log = Frame(F_side)
    F_log.isVisible = False
    p.GUI_items['F_log'] = F_log
    
    F_result = Frame(F_side)
    p.GUI_items['F_result'] = F_result
    F_result.pack(fill='both', expand=True)
    F_result.pack_forget()
    F_result.isVisible = False
    F_result.made = False
    
    
    scrollbar = Scrollbar(F_log)
    scrollbar.pack(side='right', fill='y')
    textOutput = Text(F_log, yscrollcommand=scrollbar.set, bg=bg_color)
    scrollbar.config(command=textOutput.yview)
    
    p._setTextFuncs()
    for func in ('warn', 'err', 'info', 'disp', 'hint', 'pWarn'):
        setattr(p, func, updated_output(getattr(p, func), textOutput))
    
    if p.managerTextOutput is not False and p.managerTextOutput in ('right', 'left'):
        textSide = p.managerTextOutput
        if p.managerTextOutput == 'right': 
            F0_side = 'left'
    
    textOutput.pack(expand=True, fill='both')
    F_log.isVisible = True
    if p.managerTextOutput is False:
        F_side.pack_forget()
        F_side.isVisible = False
        F_log.isVisible = False
        
    F_log.pack(fill='both', expand=True)
    
    F0.pack(side=F0_side, fill='both', expand=True)
    F_side.pack(side=textSide, fill='both', expand=True)
    F_side.isVisible = True
    
    
    """                                               Title                                                """
    #root.wm_title('OpenOpt  ' + ooversion)
    

    """                                              Buttons                                               """

    '''                              Label                          '''
    ButtonsColumn = Frame(F0)
    ButtonsColumn.pack(ipady=4, expand=True)
    
    Label(ButtonsColumn, text=' OpenOpt ' + ooversion + ' ').pack(expand=True, fill='x')
    Label(ButtonsColumn, text=' Solver: ' + (p.solver if isinstance(p.solver, str) else p.solver.__name__) + ' ').pack(expand=True, fill='x')
    Label(ButtonsColumn, text=' Problem: ' + p.name + ' ').pack(expand=True, fill='x')
    #TODO: mb use Menubutton 

    #Statistics
#    stat = StringVar()
#    stat.set('')
#    Statistics = Button(ButtonsColumn, textvariable = stat, command = lambda: invokeStatistics(p))

#    cw = Entry(ButtonsColumn)
#
#    
#    b = Button(ButtonsColumn, text = 'Evaluate!', command = lambda: invokeCommand(cw))
#    cw.pack(fill='x'', side='left')
#    b.pack(side='right')
        
    '''                              Run                          '''
    
    t = StringVar()
    t.set("      Run      ")
    RunPause = Button(ButtonsColumn, textvariable = t, command = lambda: invokeRunPause(p))
    RunPause.pack(ipady=15, expand=True, fill='x', pady=8)
    p.GUI_items['RunPause'] = RunPause
    p.statusTextVariable = t


    '''                              Log                          '''
        
    Log = Button(ButtonsColumn, text = '    Log    ', command = lambda:invokeLog(p))
#    Log.config(state=DISABLED)
    Log.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Log'] = Log

    '''                             Result                         '''
    
    Result = Button(ButtonsColumn, text = '   Result   ', command = lambda: invokeResult(p))
    Result.config(state=DISABLED)
    # TODO: MOP
    if p.probType in ('NLP', 'SNLE', 'NLSP', 'GLP', 'LP', 
    'MILP', 'NSP', 'MINLP', 'LLSP', 'SLE') \
    or p.probType.endswith('QP'):
        Result.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Result'] = Result

    '''                             Enough                         '''

    Enough = Button(ButtonsColumn, text = '   Enough!   ', 
                    command = lambda: invokeEnough(p))
    Enough.config(state=DISABLED)
    Enough.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Enough'] = Enough


    '''                             Exit                         '''

    Quit = Button(ButtonsColumn, text="      Exit      ", command = lambda:invokeExit(p))
    Quit.pack(ipady=15, expand=True, fill='x', pady=8)
    p.GUI_items['Quit'] = Quit
    
    '''                             Time                         '''
    Frame(ButtonsColumn).pack(ipady=0, expand=True, fill='x')
    F = Frame(ButtonsColumn)
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
    Frame(ButtonsColumn).pack(ipady=0, expand=True, fill='x')
    F = Frame(ButtonsColumn)
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
########################################################
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
        
########################################################
def doCalculations(p):
    p._immutable = False
    try:
        p.__dict__['tmp_result'] = p.solve(*p._args, **p._kwargs)
    except killThread:
        if p.plot and hasattr(p, 'figure'):
            #p.figure.canvas.draw_drawable = lambda: None
            try:
                import pylab
                pylab.ioff()
                pylab.close('all')
            except:
                pass
#    p._immutable = True
    p.GUI_items['Result'].config(state='active')
    p.GUI_items['RunPause'].config(state=DISABLED)
    p.GUI_items['Enough'].config(state=DISABLED)
#    p.GUI_items['Quit'].config(state='active')
        

########################################################
#def invokeStatistics(p):
def invokeCommand(cw):
    exec(cw.get())
    
########################################################
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
    
########################################################
def invokeResult(p):
    res = w = p.GUI_items['F_result']
    log = p.GUI_items['F_log']
    side = p.GUI_items['F_side']
    
#    p.disp('%s %s' % (side.isVisible, res.isVisible))
    
    if not w.made: 
        C = Frame(w)
        p.GUI_items['ResultRepr'] = C
        C.pack(side='bottom', fill='x', expand=True)
        
        R = Text(w, bg=p._bg_color)
        R.pack(side = 'left', expand=True, fill='both')
        scrollbar = Scrollbar(w)
        scrollbar.pack(side='right', fill='y')
        
        r = p.tmp_result
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
        w.made = True
        
    if side.isVisible:
        if res.isVisible:
            withdraw(res, side)
        else:
            restore(res)
    else:
        restore(side, res)
    withdraw(log)
    
########################################################
def invokeExit(p):
    p._immutable = False
    p.userStop = True
    p.istop = USER_DEMAND_EXIT
    if hasattr(p, 'stopdict'): 
        p.stopdict[USER_DEMAND_EXIT] = True

    # however, the message is currently unused
    # since openopt return r = None
    p.msg = 'user pressed Exit button'

    p.GUI_root.destroy()

########################################################
def invokeLog(p):
    log = p.GUI_items['F_log']
    res = p.GUI_items['F_result']
    side = p.GUI_items['F_side']
    
    withdraw(res)
    if side.isVisible:
        if log.isVisible:
            revert(side)
        else:
            restore(log)
    else:
        restore(side, log)
        
########################################################
def invokeEnough(p):
    
    p.userStop = True
    p.istop = BUTTON_ENOUGH_HAS_BEEN_PRESSED
    if hasattr(p, 'stopdict'):  
        p.stopdict[BUTTON_ENOUGH_HAS_BEEN_PRESSED] = True
    p.msg = 'button Enough has been pressed'

    if p.state == 'paused':
        invokeRunPause(p, isEnough=True)
    else:
        p.GUI_items['RunPause'].config(state=DISABLED)
        p.GUI_items['Enough'].config(state=DISABLED)
        p.GUI_items['Quit'].config(state=DISABLED)
        
########################################################
def revert(*args):
    for w in args:
        status = w.isVisible
        if status:
            w.pack_forget()
            w.isVisible = False
        else:
            w.pack()
            w.isVisible = True

########################################################
def restore(*args):
    for w in args:
        status = w.isVisible
        if status is False:
            w.pack()
            w.isVisible = True
        
########################################################
def withdraw(*args):
    for w in args:
        status = w.isVisible
        if status:
            w.pack_forget()
            w.isVisible = False
