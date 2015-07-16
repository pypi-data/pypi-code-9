import inspect
from baseClasses import OOArray

def print_info(oof):
    Str = '-'*15 + ' FuncDesigner info on initialization of object with id %d ' % oof._id + '-'*15 
    print('\n'+Str)
    print('type: %s' % type(oof))
    if isinstance(oof, OOArray):
        print('ooarray %s' % oof.name)
        if not oof._is_array_of_oovars:
            print('ooarray expression: %s' % oof.name)
    else: # oofun, mb oovar
        if oof.is_oovar:
            print('oovar %s' % oof.name)
        else:
            print('oofun %s' % oof.name)
            print('oofun expression: %s' % oof.expr)
    print('Stack info:')
    for frame_tuple in inspect.stack()[2:]:
        # minor optimization for Eric Python IDE
        if 'dist-packages' in frame_tuple[1] and 'eric'in frame_tuple[1]:
            break
        print('%s, line %d, in %s' % frame_tuple[1:4])
        for elem in frame_tuple[4]:
            print('\t\t%s' % elem)
    print('_'*len(Str))

class FD_trace_id:
    ids = []
    object = {}
    def __init__(self):
        pass
    def __call__(self, *args, **kw):
        assert len(kw) == 0 and len(args) == 1
        self.ids = args[0] if type(args[0]) in (list, tuple) else [args[0]]
    has = lambda self, val: val in self.ids

fd_trace_id = FD_trace_id()
