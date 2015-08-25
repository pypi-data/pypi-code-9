"""
Created on Mar 13, 2015

@author: Jason Bowles
"""
import sys
import os
import importlib

def get_class(py_source):
        """
        Try to import python code dynamically
        The trick is that this may be code added at any time by any user from any path
        If there is a path seperator in dynamic path.. then we need to append it to the path
        """
        backs = '\\'
        forwards = '/'
        from_path = False
        path = ""
        if py_source.find(backs) > -1:
            mod_src = py_source.split(backs)[-1]
            from_path = True 
        elif py_source.find(forwards) > -1:
            mod_src = py_source.split(forwards)[-1]
            from_path = True
    
        if from_path:
            print 'found path for.. '+mod_src
            path =  py_source[:py_source.find(mod_src)-1]
            print 'path is.. '+path
            sys.path.append(os.pathsep+path)
        else:
            mod_src = py_source
    
        class_data = mod_src.split(".")
        class_str = class_data[-1]
        src_mod = '.'.join(class_data[:len(class_data)-1])  
        module = importlib.import_module(src_mod)
        class_ = getattr(module, class_str)
        return class_

def load_class(class_):
    options = {}
    options['name'] = 'test'
    options['entry'] = 'test'
    return class_(options)


